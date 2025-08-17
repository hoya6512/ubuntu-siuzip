from os.path import splitext
from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str

from accounts.models import User


class Tag(models.Model):
    tag_name = models.CharField("태그명", max_length=120, unique=True)

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    category_name = models.CharField("카테고리명", max_length=120, unique=True)
    category_slug = models.SlugField(
        "카테고리 설명", max_length=120, null=True, blank=True, allow_unicode=True
    )

    def __str__(self):
        return self.category_name


def uuid_name_upload_to(instance: models.Model, filename: str) -> str:
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    ymd_path = force_str(timezone.now().strftime("%Y/%m/%d/"))
    extension = splitext(filename)[-1].lower()
    new_filename = uuid4().hex + extension
    return "/".join((app_label, cls_name, ymd_path, new_filename))


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    tags = models.ManyToManyField(Tag, verbose_name="태그", blank=True)
    like_users = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    category = models.ForeignKey(
        Category, verbose_name="카테고리", on_delete=models.CASCADE
    )
    thumbnail = models.ImageField(
        blank=True,
        null=True,
        # upload_to="blog/thumbnails/%Y/%m/%d",
        upload_to=uuid_name_upload_to,
    )
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", args=[self.pk])

    def __str__(self):
        return "%s - %s" % (self.author, self.title)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    target = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="대상 게시글"
    )
    like_users = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.content, self.author)


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    target_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name="대상 댓글"
    )
    like_users = models.ManyToManyField(User, related_name="liked_replies", blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.content, self.author)
