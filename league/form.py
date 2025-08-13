from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from league.models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            "name",
            "pl_team",
            "pl_pot",
            "ll_team",
            "ll_pot",
            "bl_team",
            "bl_pot",
            "sa_team",
            "sa_pot",
            "cup_point",
        ]

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.add_input(Submit("submit", "저장", css_class="w-100"))
