import requests
import asyncio
import aiohttp
import time
# import sys
# sys.path.append("/home/argi/PycharmProjects/KBAData")

from project.utils.webscraping.pages.box_score_page import BoxScorePage
from project.utils.webscraping.pages.team_page import TeamPage
from project.utils.webscraping.parsers.box_score_parser import BoxScoreParser
from project.utils.webscraping.parsers.team_parser import TeamParser
from project.utils.webscraping.pages.player_stats_page import PlayerStatsPage
from project.utils.csv_module import CsvWriter

INITIAL_URL = "https://www.basketball-reference.com"
TEAMS = {}
DATA = []


async def download_team_site(session, team_name, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))
        TEAMS[team_name] = TeamPage(await response.text()).roster


async def download_all_team_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for team_name, url in sites.items():
            task = asyncio.ensure_future(download_team_site(session, team_name, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


async def download_player_site(session, team, player_name, url, player_statistics):
    async with session.get(url) as response:
        print(f"Downloading stats for player: {player_name} from: {url}")
        player_statistics[player_name] = PlayerStatsPage(await response.text()).statistics
        for player, stats in player_statistics.items():
            for season_stat in stats:
                row = [player, team] + list(stat for stat in season_stat.values())
                DATA.append(row)


async def download_all_player_sites(teams_data):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for team, player_sites in teams_data.items():
            for player_name, url in player_sites.items():
                player_statistics = {}
                task = asyncio.ensure_future(
                    download_player_site(session, team, player_name, url, player_statistics))
                tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def download_player_stats_for_header(teams_data):
    for team, player_sites in teams_data.items():
        for player_name, url in player_sites.items():
            response = requests.request("GET", f"{url}")
            statistics_header = PlayerStatsPage(response.content).statistics_header
            return statistics_header
        break


def get_box_scores():
    response = requests.request("GET", f"{INITIAL_URL}/boxscores")
    return response.content


def get_roster(teams):
    team_sites = {}
    for team in teams:
        for team_name, team_uri in team.items():
            team_sites[team_name] = f"{INITIAL_URL}{team_uri}"
    asyncio.get_event_loop().run_until_complete(download_all_team_sites(team_sites))


def get_teams_data():
    teams_data = {}
    for team, players_html in TEAMS.items():
        player_sites = {}
        players = TeamParser(players_html).get_players
        for player in players:
            for player_name, player_uri in player.items():
                player_sites[player_name] = f"{INITIAL_URL}{player_uri}"
        teams_data[team] = player_sites
    return teams_data


def get_player_stats(teams_data):
    asyncio.get_event_loop().run_until_complete(download_all_player_sites(teams_data))


def main():
    start_time = time.time()
    box_scores_page = get_box_scores()
    teams_html = BoxScorePage(box_scores_page).teams
    teams = BoxScoreParser(teams_html).get_teams

    get_roster(teams)
    teams_data = get_teams_data()
    get_player_stats(teams_data)
    header = download_player_stats_for_header(teams_data)
    print(header)
    DATA.insert(0, header)
    writer = CsvWriter("player_stats_avg.csv")
    writer.write(DATA)

    duration = time.time() - start_time
    print(f"Downloaded from {len(list(TEAMS.items()))} teams, {len(DATA)} player stats in {duration} seconds")


if __name__ == '__main__':
    main()
