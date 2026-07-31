from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """Admin-facing form for creating/editing an Event."""

    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "location",
            "event_date",
            "start_time",
            "end_time",
            "image",
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Annual General Meeting"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "What's this event about?"}),
            "location": forms.TextInput(attrs={"placeholder": "e.g. BLUS Community Hall, Beijing"}),
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shared dashboard input styling (see .form-input in static/css/main.css).
        for name, field in self.fields.items():
            if name == "image":
                field.widget.attrs.setdefault("class", "form-input-file")
            else:
                field.widget.attrs.setdefault("class", "form-input")
        self.fields["description"].required = False
        self.fields["location"].required = False
        self.fields["start_time"].required = False
        self.fields["end_time"].required = False

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and end_time <= start_time:
            self.add_error("end_time", "End time must be after the start time.")
        return cleaned_data
