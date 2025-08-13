from django.contrib import admin

from schedule.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
