import requests
import asyncio
import aiohttp

from project.utils.webscraping.pages.box_score_page import BoxScorePage
from project.utils.webscraping.pages.team_page import TeamPage
from project.utils.webscraping.parsers.box_score_parser import BoxScoreParser
from project.utils.webscraping.parsers.team_parser import TeamParser
from project.utils.webscraping.pages.player_stats_page import PlayerStatsPage
from project.utils.csv_module import CsvWriter

INITIAL_URL = "https://www.basketball-reference.com/"


def get_box_scores():
    response = requests.request("GET", f"{INITIAL_URL}/boxscores")
    return response.content


def get_roster(team_uri):
    print(f"get_roster for {INITIAL_URL}{team_uri}")
    response = requests.request("GET", f"{INITIAL_URL}{team_uri}")
    return response.content


def get_statistics(player_uri):
    print(f"get_player_stats for {INITIAL_URL}{player_uri}")
    response = requests.request("GET", f"{INITIAL_URL}{player_uri}")
    return response.content


def main():
    box_scores_page = get_box_scores()
    teams_html = BoxScorePage(box_scores_page).teams
    teams = BoxScoreParser(teams_html).get_teams
    data = []
    for team in teams[-1:]:
        for team_name, team_uri in team.items():
            players_page = get_roster(team_uri)
            roster_html = TeamPage(players_page).roster
            players = TeamParser(roster_html).get_players
            for player in players:
                for player_name, player_uri in player.items():
                    print(f"{player_name} - {team_name} - {player_uri}")
                    statistics_page = get_statistics(player_uri)
                    statistics = PlayerStatsPage(statistics_page).statistics
                    print(f"{player_name};{team_name};{player_uri};{statistics}")
                    for row in statistics:
                        data.append(row.values())

    writer = CsvWriter("testExport.csv")
    writer.write(data)


if __name__ == '__main__':
    main()
