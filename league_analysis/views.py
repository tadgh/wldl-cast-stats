from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from league_analysis.models import TeamRollingStatistics, Team
# Create your views here.

def live_data(request):
    if request.method == "GET":
        return "hi!"

def head_to_head(request):
    team_one_stats = TeamRollingStatistics.objects.get(team__name="The Mike Gleesons")
    team_two_stats = TeamRollingStatistics.objects.get(team__name="Sink Catz")
    context = {
        "team_one_statistics": team_one_stats,
        "team_two_statistics": team_two_stats
    }
    return render(request, "leagueanalysis/headtohead.html",context)

def css_demo(request):
    return render(request, "leagueanalysis/cssexample.html", {})
