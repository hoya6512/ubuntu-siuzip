from django.urls import include, path
from . import views

app_name = "memo"


urlpatterns = [
    path("", views.index, name="index"),
    path("status/<str:status>/", views.index_status, name="index_status"),
    path("new/", views.memo_new, name="memo_new"),
    path("<int:pk>/edit/", views.memo_edit, name="memo_edit"),
    path("<int:pk>/delete/", views.memo_delete, name="memo_delete"),
    path(
        "<int:pk>/change_statue/", views.memo_change_status, name="memo_change_status"
    ),
    path("<int:pk>/like/", views.memo_like, name="memo_like"),
]
