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


def add_avatar_urls():
    avatars = {}
    #aspiring divines
    avatars["7358194"] = "https://i.imgur.com/qrL7QKa.jpg"
    #average joes
    avatars["7405334"] = "http://notsportscenter.com/wp-content/uploads/2013/04/averagejoes.jpg"
    #critmode squad
    avatars["2448842"] = "https://i.imgur.com/G1OPBb9.png"
    #DNPWPD
    avatars["7389684"] = "https://cdn.discordapp.com/attachments/614534838799826949/615606291716636675/Donotpetimplayingdota.PNG"
    #flavortown
    avatars["7370154"] = "https://i.kym-cdn.com/photos/images/original/001/034/121/a48.png"
    #GGS
    avatars["7359390"] = "https://i.imgur.com/QkMEERU.png"
    #Lothars Edgelords
    avatars["7387455"] = "https://crystal-cdn4.crystalcommerce.com/photos/887835/BetrayaloftheGuardian_US_182.jpg"
    #Mango Tangoes
    avatars["2469166"] = "https://i.imgur.com/iYVWz6Y.png"
    #Marcos Angels
    avatars["7373580"] = "https://i.imgur.com/eOnnnpx.png"
    #Nice and Successful
    avatars["6322029"] = "https://i.imgur.com/GuOMtLY.jpg"
    #Praetotors
    avatars["7375898"] = "https://us.v-cdn.net/5020300/uploads/FileUpload/74/b817fb1bd061e517e232dcd226941e.jpg"
    #Sink Catz
    avatars["7387458"] = "https://i.ibb.co/q95L6k2/SinkCatz.jpg"
    #SOTA
    avatars["7341964"] = "https://cdn.discordapp.com/attachments/613048450355036215/613158300124577905/Sons_of_The_Ancient.png"
    #TeamTempus
    avatars["5160519"] = "https://i.ibb.co/NFMn18f/Tempus-v6.jpg"
    #TTEH
    avatars["7408356"] = "https://cdn.discordapp.com/attachments/609193204264468480/616065428766326785/Tempus_Eh.png"
    #TMG
    avatars["7374310"] = "https://i.imgur.com/3s8kIcD.png?1"
    #3Jm
    avatars["7327646"] = "https://i.ibb.co/Hq6sVZ2/3JM-Logo.png"
    #TTU
    avatars["7341964"] = "https://media.discordapp.net/attachments/477290531173695490/477290761751101450/ttu_esports_logo.png"
    #WMR
    avatars["7331032"] = "https://media.discordapp.net/attachments/612692659194036234/612692999645954064/walllon_raduie.jpg"

    for team_id, url in tqdm(avatars.items()):
        team = Team.objects.get(id=team_id)
        team.logo_image_url = url
        team.save()


def seed_server():
    update_heroes()
    scrape_and_recalculate_league_data()
    add_avatar_urls()
