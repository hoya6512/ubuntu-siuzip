from django.urls import include, path
from . import views

app_name = "schedule"


urlpatterns = [
    path("", views.index, name="calendar"),
    path("event/<int:pk>", views.event_detail, name="event_detail"),
    path("event/new", views.event_new, name="event_new"),
    path("event/edit/<int:pk>", views.event_edit, name="event_edit"),
    path("event/delete/<int:pk>", views.event_delete, name="event_delete"),
]
