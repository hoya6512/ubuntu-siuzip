from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("user/edit/", views.user_edit, name="user_edit"),
    path("user/password_edit/", views.password_edit, name="password_edit"),
    path("profile/posted", views.profile_posted, name="profile_posted"),
    path("profile/commented", views.profile_commented, name="profile_commented"),
    path("profile/reply", views.profile_reply, name="profile_reply"),
]
