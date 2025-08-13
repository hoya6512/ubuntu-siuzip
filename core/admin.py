from django.contrib import admin

from memo.models import Memo


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ["title"]
