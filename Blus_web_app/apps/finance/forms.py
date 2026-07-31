from django import forms
from django.utils import timezone

from apps.students.models import StudentProfile

from .models import Due, Loan


class DueForm(forms.ModelForm):
    """Admin-facing form for creating/editing a student's due payment."""

    class Meta:
        model = Due
        fields = ("student", "title", "amount", "due_date", "is_paid", "paid_date", "notes")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. 2026 Annual Membership Due"}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0", "placeholder": "0.00"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "paid_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Optional notes for this due"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = StudentProfile.objects.select_related("user")
        self.fields["notes"].required = False
        self.fields["paid_date"].required = False
        for name, field in self.fields.items():
            if name == "is_paid":
                continue
            field.widget.attrs.setdefault("class", "form-input")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("is_paid") and not cleaned_data.get("paid_date"):
            cleaned_data["paid_date"] = timezone.now().date()
        return cleaned_data


class LoanForm(forms.ModelForm):
    """Admin-facing form for creating/editing a student's loan."""

    class Meta:
        model = Loan
        fields = ("student", "purpose", "amount", "amount_repaid", "issued_date", "due_date", "status", "notes")
        widgets = {
            "purpose": forms.TextInput(attrs={"placeholder": "e.g. Emergency housing assistance"}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0", "placeholder": "0.00"}),
            "amount_repaid": forms.NumberInput(attrs={"step": "0.01", "min": "0", "placeholder": "0.00"}),
            "issued_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Optional notes for this loan"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = StudentProfile.objects.select_related("user")
        self.fields["amount_repaid"].required = False
        self.fields["due_date"].required = False
        self.fields["notes"].required = False
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-input")

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        amount_repaid = cleaned_data.get("amount_repaid")
        if amount is not None and amount_repaid is not None and amount_repaid > amount:
            self.add_error("amount_repaid", "Amount repaid can't exceed the loan amount.")
        return cleaned_data
