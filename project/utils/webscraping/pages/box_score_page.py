from bs4 import BeautifulSoup
from project.utils.webscraping.parsers.box_score_parser import BoxScoreParser


class BoxScorePage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def teams(self):
        return BoxScoreParser(self.soup).get_team_rows
