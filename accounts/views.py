from typing import Optional

from django.contrib import messages
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, RedirectURLMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import (
    LoginForm,
    SignupForm,
    ProfileForm,
    UserUpdateForm,
    UserPasswordChangeForm,
)
from accounts.models import User, Profile
from blog.models import Post, Comment, Reply


class SignupView(RedirectURLMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "회원가입",
    }
    success_url = reverse_lazy("accounts:profile")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to != request.path:
                messages.warning(request, "이미 로그인 되어 있습니다.")
                return HttpResponseRedirect(redirect_to)
        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "회원가입을 환영합니다!")

        user = self.object
        auth_login(self.request, user)
        messages.success(self.request, "회원가입과 동시에 로그인 지원")

        return response


signup = SignupView.as_view()


class LoginView(DjangoLoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "로그인",
    }


login = LoginView.as_view()


class LogoutView(DjangoLogoutView):
    next_page = "accounts:login"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "로그아웃 완료.")
        return response


logout = LogoutView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "프로필 사진 수정"}
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None) -> Optional[Profile]:
        if not self.request.user.is_authenticated:
            return None

        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "프로필을 저장하였습니다.")
        return response


profile_edit = ProfileUpdateView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "닉네임 수정"}
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None) -> Optional[User]:
        if not self.request.user.is_authenticated:
            return None

        try:
            return self.request.user
        except User.DoesNotExist:
            return None

    def form_valid(self, form):
        user = form.save(commit=False)
        profile.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "프로필을 저장하였습니다.")
        return response


user_edit = UserUpdateView.as_view()


@login_required
def password_edit(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect("accounts:profile")
    else:
        form = UserPasswordChangeForm(user=request.user)

    return render(
        request, "crispy_form.html", {"form_title": "비밀번호 변경", "form": form}
    )


@login_required
def profile_posted(request):

    posts = Post.objects.filter(author=request.user)
    page = request.GET.get("page", "1")

    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)

    context = {
        "blog_list": page_obj,
    }

    return render(request, "accounts/profile_posted.html", context)


@login_required
def profile_commented(request):

    comments = Comment.objects.filter(author=request.user)
    page = request.GET.get("page", "1")

    paginator = Paginator(comments, 5)
    page_obj = paginator.get_page(page)

    context = {
        "comment_list": page_obj,
    }

    return render(request, "accounts/profile_commented.html", context)


@login_required
def profile_reply(request):

    replies = Reply.objects.filter(author=request.user)
    page = request.GET.get("page", "1")

    paginator = Paginator(replies, 5)
    page_obj = paginator.get_page(page)

    context = {
        "reply_list": page_obj,
    }

    return render(request, "accounts/profile_reply.html", context)
