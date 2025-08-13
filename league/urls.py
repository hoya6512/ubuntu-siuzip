from django.urls import path
from . import views

app_name = "league"


urlpatterns = [
    path("", views.league_standings, name="league_standings"),
    path(
        "league_create/<int:league_id>",
        views.create_league_data,
        name="create_league_data",
    ),
    path(
        "league_update/<int:league_id>",
        views.update_league_data,
        name="update_league_data",
    ),
    path("league_create_all/", views.create_league_data_all, name="league_create_all"),
    path("league_update_all/", views.update_league_data_all, name="league_update_all"),
    path("player/", views.player_list, name="player_list"),
    path("player/new", views.player_new, name="player_new"),
    path("player/edit/<int:pk>", views.player_edit, name="player_edit"),
    path("player/update", views.update_player_data, name="update_player_data"),
]
