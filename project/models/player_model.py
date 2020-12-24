from project.models.statistics_model import StatisticsModel


class PlayerModel:
    def __init__(
            self, name: str,
            team: str,
            position: str,
            statistics: StatisticsModel
    ):
        self.name = name
        self.team = team
        self.position = position
        self.statistics = statistics

    def __repr__(self):
        return f"{self.name};{self.team};{self.position};{self.statistics.__repr__}"
