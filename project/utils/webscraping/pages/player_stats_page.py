from bs4 import BeautifulSoup
from typing import List

from project.utils.webscraping.parsers.players_stats_parser import PlayerParser


class PlayerStatsPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def statistics(self) -> List:
        statistics_table = self.soup.find("table", {"id": "per_game"})
        return PlayerParser(statistics_table).player_stats

    @property
    def statistics_header(self) -> List:
        statistics_table = self.soup.find("table", {"id": "per_game"})
        return PlayerParser(statistics_table).get_statistics_header
