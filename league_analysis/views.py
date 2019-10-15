from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from league_analysis.models import TeamRollingStatistics, Team
# Create your views here.

def live_data(request):
    if request.method == "GET":
        return "hi!"

def head_to_head(request):
    team_stats = TeamRollingStatistics.objects.get(team__name="The Mike Gleesons")
    context = {
        "team_one_statistics": team_stats
    }
    #TODO STYLE THIS
    return render(request, "leagueanalysis/headtohead.html",context)
