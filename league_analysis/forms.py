from django import forms

from league_analysis.models import Team


class TeamSelectForm(forms.Form):
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), required=True)


