from os.path import splitext
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.encoding import force_str


def uuid_name_upload_to(instance: models.Model, filename: str) -> str:
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    ymd_path = force_str(timezone.now().strftime("%Y/%m/%d/"))
    extension = splitext(filename)[-1].lower()
    new_filename = uuid4().hex + extension
    return "/".join((app_label, cls_name, ymd_path, new_filename))


class PremierLeague(models.Model):
    team_name = models.CharField("팀이름", max_length=120)
    team_logo_server = models.URLField("서버로고주소")
    team_logo = models.ImageField(
        blank=True,
        null=True,
        upload_to=uuid_name_upload_to,
    )
    team_id = models.CharField("팀ID", max_length=120, unique=True)
    rank = models.IntegerField("순위")
    played = models.IntegerField("경기")
    points = models.IntegerField("승점")
    win = models.IntegerField("승")
    draw = models.IntegerField("무")
    lose = models.IntegerField("패")
    goals_for = models.IntegerField("득점")
    goals_against = models.IntegerField("실점")
    goals_diff = models.IntegerField("득실")
    recent = models.CharField("최근경기", max_length=120, blank=True, null=True)
    uefa = models.CharField("유럽대항전", max_length=120, blank=True, null=True)
    updated_from_server = models.DateTimeField("업데이트시간", blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.team_name, self.team_id)

    class Meta:
        ordering = ["rank"]


class LaLiga(models.Model):
    team_name = models.CharField("팀이름", max_length=120)
    team_logo_server = models.URLField("서버로고주소")
    team_logo = models.ImageField(
        blank=True,
        null=True,
        upload_to=uuid_name_upload_to,
    )
    team_id = models.CharField("팀ID", max_length=120, unique=True)
    rank = models.IntegerField("순위")
    played = models.IntegerField("경기")
    points = models.IntegerField("승점")
    win = models.IntegerField("승")
    draw = models.IntegerField("무")
    lose = models.IntegerField("패")
    goals_for = models.IntegerField("득점")
    goals_against = models.IntegerField("실점")
    goals_diff = models.IntegerField("득실")
    recent = models.CharField("최근경기", max_length=120, blank=True, null=True)
    uefa = models.CharField("유럽대항전", max_length=120, blank=True, null=True)
    updated_from_server = models.DateTimeField("업데이트시간", blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.team_name, self.team_id)

    class Meta:
        ordering = ["rank"]


class BundesLiga(models.Model):
    team_name = models.CharField("팀이름", max_length=120)
    team_logo_server = models.URLField("서버로고주소")
    team_logo = models.ImageField(
        blank=True,
        null=True,
        upload_to=uuid_name_upload_to,
    )
    team_id = models.CharField("팀ID", max_length=120, unique=True)
    rank = models.IntegerField("순위")
    played = models.IntegerField("경기")
    points = models.IntegerField("승점")
    win = models.IntegerField("승")
    draw = models.IntegerField("무")
    lose = models.IntegerField("패")
    goals_for = models.IntegerField("득점")
    goals_against = models.IntegerField("실점")
    goals_diff = models.IntegerField("득실")
    recent = models.CharField("최근경기", max_length=120, blank=True, null=True)
    uefa = models.CharField("유럽대항전", max_length=120, blank=True, null=True)
    updated_from_server = models.DateTimeField("업데이트시간", blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.team_name, self.team_id)

    class Meta:
        ordering = ["rank"]


class SerieA(models.Model):
    team_name = models.CharField("팀이름", max_length=120)
    team_logo_server = models.URLField("서버로고주소")
    team_logo = models.ImageField(
        blank=True,
        null=True,
        upload_to=uuid_name_upload_to,
    )
    team_id = models.CharField("팀ID", max_length=120, unique=True)
    rank = models.IntegerField("순위")
    played = models.IntegerField("경기")
    points = models.IntegerField("승점")
    win = models.IntegerField("승")
    draw = models.IntegerField("무")
    lose = models.IntegerField("패")
    goals_for = models.IntegerField("득점")
    goals_against = models.IntegerField("실점")
    goals_diff = models.IntegerField("득실")
    recent = models.CharField("최근경기", max_length=120, blank=True, null=True)
    uefa = models.CharField("유럽대항전", max_length=120, blank=True, null=True)
    updated_from_server = models.DateTimeField("업데이트시간", blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.team_name, self.team_id)

    class Meta:
        ordering = ["rank"]


class Player(models.Model):
    name = models.CharField("이름", max_length=100)
    pl_team = models.ForeignKey(
        PremierLeague, verbose_name="PL팀", on_delete=models.CASCADE
    )
    ll_team = models.ForeignKey(LaLiga, verbose_name="LL팀", on_delete=models.CASCADE)
    bl_team = models.ForeignKey(
        BundesLiga, verbose_name="BL팀", on_delete=models.CASCADE
    )
    sa_team = models.ForeignKey(SerieA, verbose_name="SA팀", on_delete=models.CASCADE)
    pl_pot = models.CharField("PL포트", max_length=100)
    ll_pot = models.CharField("LL포트", max_length=100)
    bl_pot = models.CharField("BL포트", max_length=100)
    sa_pot = models.CharField("SA포트", max_length=100)
    cup_point = models.IntegerField("컵포인트", default=0)
    total_point = models.IntegerField("총승점", default=0)
    total_game = models.IntegerField("총경기", default=0)
    total_win = models.IntegerField("총승", default=0)
    total_draw = models.IntegerField("총무", default=0)
    total_lose = models.IntegerField("총패", default=0)
    total_goal_diff = models.IntegerField("총득실", default=0)

    class Meta:
        ordering = ["-total_point", "-total_goal_diff"]

    def __str__(self):
        return "%s" % (self.name)
