from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
import http.client
import json

from django.urls import reverse_lazy
from django.views.generic import CreateView

from league.form import PlayerForm
from league.models import PremierLeague, LaLiga, BundesLiga, SerieA, Player

league_dict = {39: "프리미어리그", 140: "라리가", 78: "분데스리가", 135: "세리에A"}
league_dict_for_query = {
    39: PremierLeague,
    140: LaLiga,
    78: BundesLiga,
    135: SerieA,
}


def index(request):
    pass


def league_standings(request):
    pl_standings = PremierLeague.objects.all()
    ll_standings = LaLiga.objects.all()
    bl_standings = BundesLiga.objects.all()
    sa_standings = SerieA.objects.all()
    player = Player.objects.all()

    context = {
        "pl_standings": pl_standings,
        "ll_standings": ll_standings,
        "bl_standings": bl_standings,
        "sa_standings": sa_standings,
        "player_list": player,
    }

    return render(request, "league/index.html", context)


def create_league_data(request, league_id):

    if league_dict_for_query[league_id].objects.exists():
        messages.error(
            request,
            league_dict[league_id] + " 데이터 생성 불가(기존 데이터 삭제 후 생성 필요)",
        )
    else:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": "52d1b79add89f9d721330e87e2ca76d3",
        }
        conn.request(
            "GET",
            "/standings?league=" + str(league_id) + "&season=2025",
            headers=headers,
        )

        res = conn.getresponse()
        data = res.read()

        get_json = json.loads(data)["response"][0]["league"]["standings"][0]

        for team_data in get_json:
            league_dict_for_query[league_id].objects.create(
                rank=team_data["rank"],
                team_name=team_data["team"]["name"],
                team_logo_server=team_data["team"]["logo"],
                team_id=team_data["team"]["id"],
                played=team_data["all"]["played"],
                points=team_data["points"],
                win=team_data["all"]["win"],
                draw=team_data["all"]["draw"],
                lose=team_data["all"]["lose"],
                goals_for=team_data["all"]["goals"]["for"],
                goals_against=team_data["all"]["goals"]["against"],
                goals_diff=team_data["goalsDiff"],
                recent=team_data["form"],
                uefa=team_data["description"],
                updated_from_server=team_data["update"],
            )
        messages.success(request, league_dict[league_id] + " 데이터 생성 완료.")
    return redirect("league:league_standings")


def create_league_data_all(request):
    create_league_data(request, 39)
    create_league_data(request, 140)
    create_league_data(request, 78)
    create_league_data(request, 135)

    return redirect("league:league_standings")


def update_league_data(request, league_id):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": "52d1b79add89f9d721330e87e2ca76d3",
    }
    conn.request(
        "GET", "/standings?league=" + str(league_id) + "&season=2025", headers=headers
    )

    res = conn.getresponse()
    data = res.read()

    get_json = json.loads(data)["response"][0]["league"]["standings"][0]

    for team_data in get_json:
        league_dict_for_query[league_id].objects.filter(
            team_id=team_data["team"]["id"]
        ).update(
            rank=team_data["rank"],
            points=team_data["points"],
            played=team_data["all"]["played"],
            win=team_data["all"]["win"],
            draw=team_data["all"]["draw"],
            lose=team_data["all"]["lose"],
            goals_for=team_data["all"]["goals"]["for"],
            goals_against=team_data["all"]["goals"]["against"],
            goals_diff=team_data["goalsDiff"],
            recent=team_data["form"],
            uefa=team_data["description"],
            updated_from_server=team_data["update"],
        )
    messages.success(request, league_dict[league_id] + " 업데이트 완료.")
    return redirect("league:league_standings")


def update_league_data_all(request):
    update_league_data(request, 39)
    update_league_data(request, 140)
    update_league_data(request, 78)
    update_league_data(request, 135)

    return redirect("league:league_standings")


def player_list(request):
    players = Player.objects.all()

    context = {"players": players}

    return render(request, "league/player_list.html", context)


class PlayerCreateView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 참가자"}
    success_url = reverse_lazy("league:player_list")

    def form_valid(self, form):
        form.save()

        response = super().form_valid(form)
        messages.success(self.request, "새 참가자가 추가 되었습니다.")
        return redirect(self.get_success_url())


player_new = PlayerCreateView.as_view()


@login_required(login_url="accounts:login")
def player_edit(request, pk):
    player = get_object_or_404(Player, pk=pk)

    if not request.user.is_superuser:
        if request.META.get("HTTP_REFERER"):
            messages.error(request, "수정권한이 없습니다.")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "수정권한이 없습니다.")
            return redirect("league:league_standings")

    if request.method == "GET":
        form = PlayerForm(instance=player)
    else:
        form = PlayerForm(data=request.POST, files=request.FILES, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, "플레이어 정보 수정 완료.")
            return redirect("league:player_list")

    return render(
        request,
        template_name="crispy_form.html",
        context={"form_title": "플레이어 정보 수정", "form": form},
    )


def update_player_data(request):
    player_data = Player.objects.all()

    for player in player_data:
        Player.objects.filter(id=player.id).update(
            total_point=player.pl_team.points
            + player.ll_team.points
            + player.bl_team.points
            + player.sa_team.points
            + player.cup_point,
            total_game=player.pl_team.played
            + player.ll_team.played
            + player.bl_team.played
            + player.sa_team.played,
            total_win=player.pl_team.win
            + player.ll_team.win
            + player.bl_team.win
            + player.sa_team.win,
            total_draw=player.pl_team.draw
            + player.ll_team.draw
            + player.bl_team.draw
            + player.sa_team.draw,
            total_lose=player.pl_team.lose
            + player.ll_team.lose
            + player.bl_team.lose
            + player.sa_team.lose,
            total_goal_diff=player.pl_team.goals_diff
            + player.ll_team.goals_diff
            + player.bl_team.goals_diff
            + player.sa_team.goals_diff,
        )
    messages.success(request, "플레이어 현황 갱신 완료.")
    return redirect("league:league_standings")
