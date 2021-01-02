from project.utils.webscraping.locators.team_locator import TeamLocator


class TeamParser:
    def __init__(self, parent):
        self.parent = parent

    @property
    def get_roster(self):
        return [
            team_row
            for team_row in self.parent.find("div", {"id": "div_roster"}).select(TeamLocator.PLAYERS)
        ]

    @property
    def get_players(self):
        players = []
        for player_row in self.parent:
            player_dictionary = {}
            player = player_row.select_one(TeamLocator.PLAYER)
            player_dictionary[player.text] = player["href"]
            players.append(player_dictionary)
        return players
