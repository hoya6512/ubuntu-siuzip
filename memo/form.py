from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.forms.widgets import DateInput
from django_summernote.widgets import SummernoteWidget

from memo.models import Memo


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ["title", "content", "status", "due_date"]
        widgets = {
            "content": SummernoteWidget(),
            "due_date": DateInput(attrs={"type": "date"}),
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
    helper.layout = Layout("title", "content", "status", "due_date")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))
