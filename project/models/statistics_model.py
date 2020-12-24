from typing import Dict


class StatisticsModel:
    def __init__(self,  statistics: Dict):
        self.statistics = statistics

    def __repr__(self):
        statistics = ""
        for stat_value in self.statistics.values():
            statistics = statistics + f"{stat_value};"
        return statistics
