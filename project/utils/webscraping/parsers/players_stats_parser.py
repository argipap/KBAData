from project.utils.webscraping.locators.player_stats_locator import PlayerStatsLocator
from typing import List


class PlayerParser:
    def __init__(self, parent):
        self.parent = parent

    @property
    def player_stats(self) -> List:
        player_statistics = []
        stat_names = [
            stat.text for stat in self.parent.select(PlayerStatsLocator.STATISTIC_NAMES)[:30]
        ]
        stat_values = []
        for season_stat in self.parent.select(PlayerStatsLocator.STATISTIC_PER_SEASON)[:30]:
            try:
                season_stat_values = [stat_value.text for stat_value in season_stat]
            except AttributeError:
                season_stat_values = []
            if len(season_stat_values) > 0:
                stat_values.append(season_stat_values) and len(season_stat_values) > 0
        for stat_value in stat_values:
            player_statistics.append(dict(zip(stat_names, stat_value)))
        return player_statistics

    @property
    def get_statistics_header(self) -> List:
        header = [
            stat.text for stat in self.parent.select(PlayerStatsLocator.STATISTIC_NAMES)
        ]
        return header
