from django.db import models

from accounts.models import User


class Memo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    like_users = models.ManyToManyField(User, related_name="liked_memo", blank=True)
    status = models.BooleanField("진행 상태", default=True)
    due_date = models.DateTimeField("기한", null=True, blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        ordering = ["-pk"]
