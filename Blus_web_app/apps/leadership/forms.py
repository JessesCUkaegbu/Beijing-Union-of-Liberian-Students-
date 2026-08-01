from django import forms

from .models import LeadershipMember


class LeadershipMemberForm(forms.ModelForm):
    """Admin-facing form for creating/editing a leadership team member."""

    class Meta:
        model = LeadershipMember
        fields = ("name", "position", "photo", "display_order", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. James Kollie"}),
            "position": forms.TextInput(attrs={"placeholder": "e.g. President"}),
            "display_order": forms.NumberInput(attrs={"min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].required = False
        for name, field in self.fields.items():
            if name == "is_active":
                continue
            if name == "photo":
                field.widget.attrs.setdefault("class", "form-input-file")
            else:
                field.widget.attrs.setdefault("class", "form-input")
