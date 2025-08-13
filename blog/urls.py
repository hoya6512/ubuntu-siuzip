from django.urls import include, path
from . import views

app_name = "blog"


urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category_name>/", views.category_view, name="category_view"),
    path("post/", views.post_new, name="post_new"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("<int:blog_pk>/comment/new/", views.comment_new, name="comment_new"),
    path("<int:comment_pk>/comment/edit/", views.comment_edit, name="comment_edit"),
    path(
        "<int:comment_pk>/comment/delete/", views.comment_delete, name="comment_delete"
    ),
    path("<int:comment_pk>/reply/new/", views.reply_new, name="reply_new"),
    path("<int:reply_pk>/reply/edit/", views.reply_edit, name="reply_edit"),
    path("<int:reply_pk>/reply/delete/", views.reply_delete, name="reply_delete"),
    path("<int:pk>/like/", views.post_like, name="post_like"),
    path("<int:comment_pk>/comment/like/", views.comment_like, name="comment_like"),
    path("<int:reply_pk>/reply/like/", views.reply_like, name="reply_like"),
]
