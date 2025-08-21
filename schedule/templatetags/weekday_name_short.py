from django import template
import datetime

register = template.Library()


@register.filter
def weekday_name_short(value):
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    try:
        return weekdays[value.weekday()]
    except:
        try:
            return weekdays[datetime.datetime.strptime(value, "%Y-%m-%d").weekday()]
        except:
            return ""
