from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField("이메일")
    nick_name = models.CharField("닉네임", max_length=30, unique=True)

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name="프로필 사진", blank=True)

    class Meta:
        verbose_name = "프로필"
        verbose_name_plural = "프로필 목록"

    def __str__(self):
        return "%s의 프로필" % self.user
