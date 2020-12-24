from bs4 import BeautifulSoup

from project.utils.webscraping.parsers.team_parser import TeamParser


class TeamPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, "html.parser")

    @property
    def roster(self):
        return TeamParser(self.soup).get_roster
