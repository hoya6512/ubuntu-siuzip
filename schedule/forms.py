from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import ModelForm, DateInput, DateTimeInput
from schedule.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "content", "start_time", "end_time"]
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            "start_time": DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_time": DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.add_input(Submit("submit", "저장", css_class="w-100"))
