from django.db import models


class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Hero(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    common_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.common_name}({self.id})"


# TODO write class for takss like: "update all data". Run it nightly or some shit
# TODO FIGURE OUT HOW TO JAM LIVE DATA INTO THAT LIVE MATCH AUTOMATICALLY. Create a new OngoingMatch, populate it with players
# Maybe via celery?

class TeamHeroPickStatistics(models.Model):
    team = models.ForeignKey(to=Team, related_name="hero_stats", on_delete=models.DO_NOTHING)
    hero = models.ForeignKey(to=Hero, related_name="pick_stats", on_delete=models.DO_NOTHING)
    pick_count = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)
    win_percent = models.FloatField(default=0)

    def __str__(self):
        return f"[team:{self.team}, hero:{self.hero}, pick_count:{self.pick_count}, win_count:{self.win_count}, win_percent:{self.win_percent}"


class TeamRollingStatistics(models.Model):
    team = models.OneToOneField(to=Team, related_name="statistics", on_delete=models.CASCADE)
    average_kills = models.FloatField(default=0)
    average_deaths = models.FloatField(default=0)
    average_assists = models.FloatField(default=0)
    average_kda = models.FloatField(default=0)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    series_played = models.IntegerField(default=0)
    series_won = models.IntegerField(default=0)
    average_creep_stats = models.FloatField(default=0)
    average_xpm = models.FloatField(default=0)
    average_gpm = models.FloatField(default=0)

    def __str__(self):
        return f"[team:{self.team}," \
               f"average_kills:{self.average_kills}," \
               f"average_deaths:{self.average_deaths}," \
               f"average_assists:{self.average_assists}," \
               f"average_kda:{self.average_kda}," \
               f"average_assists:{self.matches_played}," \
               f"matches_won:{self.matches_won}," \
               f"series_played:{self.series_played}," \
               f"series_won:{self.series_won}," \
               f"average_creep_stats:{self.average_creep_stats}," \
               f"average_xpm:{self.average_xpm}," \
               f"average_gpm:{self.average_gpm}]"


class Player(models.Model):
    steam_id_64 = models.IntegerField()
    steam_id_3 = models.IntegerField()
    player_id = models.IntegerField()
    player_name = models.CharField(max_length=255)

    def __str__(self):
        return f"[player_name:{self.player_name}," \
           f"steam_id_64:{self.steam_id_64}," \
           f"steam_id_3:{self.steam_id_3}," \
           f"player_id:{self.player_id}]"


class PlayerRollingStatistics(models.Model):
    player = models.OneToOneField(to=Player, on_delete=models.CASCADE)
    average_kills = models.FloatField(default=0)
    average_deaths = models.FloatField(default=0)
    average_assists = models.FloatField(default=0)
    average_kda = models.FloatField(default=0)
    average_creep_stats = models.FloatField(default=0)
    average_xpm = models.FloatField(default=0)
    average_gpm = models.FloatField(default=0)
    most_common_role = models.CharField(blank=True, null=True, max_length=2)

    def __str__(self):
        return f"[player:{self.player}," \
           f"average_kills:{self.average_kills}," \
           f"average_deaths:{self.average_deaths}," \
           f"average_assists:{self.average_assists}," \
           f"average_kda:{self.average_kda}," \
           f"average_creep_stats:{self.average_creep_stats}," \
           f"average_xpm:{self.average_xpm}," \
           f"average_gpm:{self.average_gpm}," \
           f"most_common_role:{self.most_common_role}]"


class OngoingMatch(models.Model):
    team_one = models.ForeignKey(to=Team, related_name="matches_as_first_team", on_delete=models.DO_NOTHING)
    team_two = models.ForeignKey(to=Team, related_name="matches_as_second_team", on_delete=models.DO_NOTHING)
    team_one_players = models.ManyToManyField(to=Player, related_name="matches_on_first_team")
    team_two_players = models.ManyToManyField(to=Player, related_name="matches_on_second_team")

    def __str__(self):
        return f"[team_one:{self.team_one}," \
               f"team_two:{self.team_two}," \
               f"team_one_players:{self.team_one_players}," \
               f"team_two_players:{self.team_two_players}]"


class FinishedMatch(OngoingMatch):
    # TODO add post-stats here
    pass
