from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from league_analysis.forms import TeamSelectForm
from league_analysis.models import TeamRollingStatistics, Team
# Create your views here.

def live_data(request):
    if request.method == "GET":
        return "hi!"

def head_to_head(request):
    team_one_id = request.GET.get("team_one")
    team_two_id = request.GET.get("team_two")
    context = {
        "team_one_statistics": TeamRollingStatistics.objects.get(team__id=team_one_id),
        "team_two_statistics": TeamRollingStatistics.objects.get(team__id=team_two_id)
    }
    return render(request, "leagueanalysis/headtohead.html",context)

def css_demo(request):
    return render(request, "leagueanalysis/cssexample.html", {})

def select_teams(request):
    if request.method == "POST":
        form = TeamSelectForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("cast:head-to-head",) + f"?team_one={form.cleaned_data['teams'][0].id}&team_two={form.cleaned_data['teams'][1].id}")
    else:
        form = TeamSelectForm()

    return render(request, "leagueanalysis/teamselection.html", {"form": form})
