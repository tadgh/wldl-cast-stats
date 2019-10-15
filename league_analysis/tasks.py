import functools
import logging
import requests
from tqdm import tqdm

from league_analysis.models import PlayerRollingStatistics, TeamRollingStatistics, Team, TeamHeroPickStatistics, Hero

logger = logging.getLogger(__name__)
league_tables_endpoint = "https://api.stratz.com/api/v1/league/10908/tables"
hero_endpoint = "https://api.stratz.com/api/v1/Hero"

@functools.lru_cache(maxsize=128)
def get_league_response():
    response = requests.get(league_tables_endpoint)
    if response.status_code == 200:
        league_response = response.json()
        return league_response
    else:
        raise RuntimeError

#@task
def scrape_and_recalculate_league_data():

    league_data = get_league_response()
    logging.info(f"League data is: {league_data}")

    for team_overview_json in tqdm(league_data["leagueTableTeam"]["overview"]):
        team_entity, created = Team.objects.get_or_create(id=team_overview_json["teamId"])
        if created:
            logger.info(f"Found a new team id! {team_entity.id}")
        # In case they have changed their names.
        # TODO MAKE SURE NAMES ARE SHOWN UP
        team_entity.name = [value["name"] for key, value in league_data["leagueTeams"].items() if key == str(team_overview_json["teamId"])][0]
        team_entity.save()

        team_stats_entity, created = TeamRollingStatistics.objects.get_or_create(team=team_entity)

        # Very few stats are available from the overview
        team_stats_entity.matches_played = team_overview_json["matchCount"]
        team_stats_entity.matches_won = team_overview_json["matchWins"]
        team_stats_entity.series_played = team_overview_json["seriesCount"]
        team_stats_entity.series_won = team_overview_json["seriesWins"]

        # Fetch the statistics node given the team id.
        team_stats_json = [team_data for team_data in league_data["leagueTableTeam"]["stats"] if team_data["teamId"] == team_overview_json["teamId"]][0]
        team_stats_entity.average_kills = team_stats_json["kills"]
        team_stats_entity.average_deaths = team_stats_json["deaths"]
        team_stats_entity.average_assists = team_stats_json["assists"]

        # Sneaky divide by zero check, for god-tier teams that dont die
        if team_stats_entity.average_deaths > 0:
            team_stats_entity.average_kda = (team_stats_entity.average_kills + team_stats_entity.average_assists ) / team_stats_entity.average_deaths
        else:
            team_stats_entity.average_kda = 9001 #Its over 9000!

        team_stats_entity.average_creep_stats = team_stats_json["cs"]
        team_stats_entity.average_xpm = team_stats_json["xpm"]
        team_stats_entity.average_gpm = team_stats_json["gpm"]

        # Store everything we've gathered
        team_stats_entity.save()

        # Now add hero pick and success stats on a per-team basis.
        team_heroes_json = [team_data["values"] for team_data in league_data["leagueTableTeam"]["heroes"] if team_data["teamId"] == team_overview_json["teamId"]][0]
        for hero in team_heroes_json:
            hero_entity = Hero.objects.get(id=hero["heroId"])

            team_hero_stat_entity, created = TeamHeroPickStatistics.objects.get_or_create(hero=hero_entity, team=team_entity)
            team_hero_stat_entity.pick_count = hero["matchCount"]
            team_hero_stat_entity.win_count = hero["matchWins"]

            if team_hero_stat_entity.pick_count > 0:
                team_hero_stat_entity.win_percent = team_hero_stat_entity.win_count / team_hero_stat_entity.pick_count

            team_hero_stat_entity.save()



def update_heroes():
    response = requests.get(hero_endpoint)
    if response.status_code == 200:
        heroes_dict = response.json()
        for hero_id, hero_info in tqdm(heroes_dict.items()):
            hero_entity, created = Hero.objects.get_or_create(id=hero_id)
            if created:
                logger.info(f"Found a new hero! -> {hero_entity}")
            hero_entity.common_name = hero_info["displayName"]
            hero_entity.save()

