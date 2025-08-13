import os

from PIL import Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.forms import ModelForm

from accounts.models import User, Profile


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "nick_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["nick_name"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            user_qs = User.objects.filter(email__iexact=email)
            if user_qs.exists():
                raise ValidationError("이미 등록된 이메일 주소 입니다.")
        return email

    def clean_nick_name(self):
        nick_name = self.cleaned_data.get("nick_name")
        if nick_name:
            user_qs = User.objects.filter(nick_name__iexact=nick_name)
            if user_qs.exists():
                raise ValidationError("이미 등록된 닉네임 입니다.")
        return nick_name

    helper = FormHelper()
    helper.attrs = {"novalidate": "true"}
    helper.layout = Layout("username", "email", "nick_name", "password1", "password2")
    helper.add_input(Submit("submit", "회원가입", css_class="w-100"))


class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.attrs = {"novalidate": "true"}
    helper.layout = Layout(
        "username",
        "password",
    )
    helper.add_input(Submit("submit", "로그인", css_class="w-100"))


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]

    helper = FormHelper()
    helper.attrs = {"novalidate": "true"}
    helper.layout = Layout("avatar")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))

    def clean_avatar(self):
        avatar_file: File = self.cleaned_data.get("avatar")
        if avatar_file:
            img = Image.open(avatar_file)
            MAX_SIZE = (512, 512)
            img.thumbnail(MAX_SIZE)
            img = img.convert("RGB")

            thumb_name = os.path.splitext(avatar_file.name)[0] + ".jpg"
            thumb_file = ContentFile(content=b"", name=thumb_name)
            img.save(thumb_file, format="JPEG")

            return thumb_file

        return avatar_file


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["nick_name"]

    helper = FormHelper()
    helper.attrs = {"novalidate": "true"}
    helper.layout = Layout("nick_name")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].label = "기존 비밀번호"
        self.fields["old_password"].widget.attrs.update(
            {
                "class": "form-control",
                "autofocus": False,
            }
        )
        self.fields["new_password1"].label = "새 비밀번호"
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["new_password1"].label = "새 비밀번호 확인"
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.add_input(Submit("submit", "비밀번호 변경하기", css_class="w-100"))
