from project.utils.webscraping.locators.player_stats_locator import PlayerStatsLocator
from typing import List


class PlayerParser:
    def __init__(self, parent):
        self.parent = parent

    @property
    def player_stats(self) -> List:
        player_statistics = []
        stat_names = [
            stat.text for stat in self.parent.select(PlayerStatsLocator.STATISTIC_NAMES)
        ]
        stat_values = []
        for season_stat in self.parent.select(PlayerStatsLocator.STATISTIC_PER_SEASON):
            try:
                season_stat_values = [stat_value.text for stat_value in season_stat]
            except AttributeError:
                season_stat_values = ["NO_STATS" for stat_value in season_stat]
            stat_values.append(season_stat_values)
        for stat_value in stat_values:
            player_statistics.append(dict(zip(stat_names, stat_value)))
        return player_statistics
