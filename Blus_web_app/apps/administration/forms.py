from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """Validates a submission from the public /contact/ page."""

    class Meta:
        model = ContactMessage
        fields = ("first_name", "last_name", "email", "subject", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].required = False
