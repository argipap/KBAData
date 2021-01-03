from bs4 import BeautifulSoup, Comment
from typing import List
from project.utils.webscraping.parsers.players_stats_parser import PlayerParser


class PlayerStatsPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    def statistics(self, category) -> List:
        tag = None
        found_comment = False
        # check for dirty html comments that do not close and remove them in order to parse correctly
        for comment in self.soup(text=lambda text: isinstance(text, Comment)):
            if 'class="table_outer_container"' in comment.string:
                tag = BeautifulSoup(comment, 'html.parser')
                found_comment = True
                break
        valid_html = tag if (found_comment and category != 'per_game') else self.soup
        statistics_table = valid_html.find("table", {"id": category, "class": "stats_table"})
        return PlayerParser(statistics_table).player_stats

    @property
    def statistics_header(self) -> List:
        statistics_table = self.soup.find("table", {"id": "per_game"})
        return PlayerParser(statistics_table).get_statistics_header
