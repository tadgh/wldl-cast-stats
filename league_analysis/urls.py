"""DotaCastStats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from league_analysis import views
app_name = "casting"
urlpatterns = [
    path("live/", views.live_data, name="live"),
    path("head-to-head/", views.head_to_head, name="head-to-head"),
    path("team-select/", views.select_teams, name="team-select"),
    path("demo/", views.css_demo, name="css-demo")
]
