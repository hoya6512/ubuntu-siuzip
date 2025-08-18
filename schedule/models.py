from django.db import models
from django.db.models.fields import CharField

from accounts.models import User
from django.urls import reverse


class Event(models.Model):
    color_choices = (
        ("text-bg-primary", "파란색"),
        ("text-bg-secondary", "회색"),
        ("text-bg-success", "초록색"),
        ("text-bg-danger", "빨간색"),
        ("text-bg-warning", "노란색"),
        ("text-bg-info", "하늘색"),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    event_color = CharField(
        "컬러", max_length=100, choices=color_choices, default="text-bg-primary"
    )
    start_time = models.DateTimeField("시작 일시")
    end_time = models.DateTimeField("종료 일시")
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    @property
    def get_html_url(self):

        url = reverse("schedule:event_detail", args=(self.id,))
        return f'<a class="badge {self.event_color} link-offset-2 link-underline link-underline-opacity-0" href="{url}"> {self.title} </a>'

    def __str__(self):
        return "%s - %s" % (self.author, self.title)
