from project.utils.webscraping.locators.box_score_locator import BoxScoreLocator


class BoxScoreParser:
    def __init__(self, parent):
        self.parent = parent

    @property
    def get_team_rows(self):
        return [
            team_row
            for team_row in self.parent.select(BoxScoreLocator.TEAMS)
        ]

    @property
    def get_teams(self):
        teams = []
        for team_row in self.parent:
            team_dictionary = {}
            team = team_row.select_one(BoxScoreLocator.TEAM)
            team_dictionary[team.text] = team["href"]
            teams.append(team_dictionary)
        return teams
