from django.contrib import admin

from league.models import PremierLeague, LaLiga, BundesLiga, SerieA, Player


@admin.register(PremierLeague)
class PremierLeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(LaLiga)
class LaLigaAdmin(admin.ModelAdmin):
    pass


@admin.register(BundesLiga)
class BundesLigaAdmin(admin.ModelAdmin):
    pass


@admin.register(SerieA)
class SerieAAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
