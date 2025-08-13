from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Post, Comment, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category", "title", "content", "thumbnail"]
        widgets = {
            "content": SummernoteWidget(),
        }

    # widgets = {
    #     "content": forms.Textarea(
    #         attrs={
    #             "id": "content_simple",
    #         }
    #     ),
    # }

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("category", "title", "content", "thumbnail")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        # widgets = {
        #     "content": forms.Textarea(
        #         attrs={
        #             "class": "input form-control",
        #             "style": "height: 100px",
        #             "placeholder": "댓글을 입력해 주세요.",
        #         }
        #     ),
        # }

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("content")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            "content",
        ]

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("content")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))
