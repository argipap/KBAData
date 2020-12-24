from bs4 import BeautifulSoup
from typing import List

from project.utils.webscraping.locators.player_stats_locator import PlayerStatsLocator
from project.utils.webscraping.parsers.players_stats_parser import PlayerParser


class PlayerStatsPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def statistics(self) -> List:
        statistics_table = self.soup.select_one(PlayerStatsLocator.STATISTICS)
        return PlayerParser(statistics_table).player_stats
