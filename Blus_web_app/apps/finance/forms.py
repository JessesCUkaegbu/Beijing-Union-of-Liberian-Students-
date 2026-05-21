from django import forms

from .models import Due, FinanceRecord, Loan


class FinanceRecordForm(forms.ModelForm):
    class Meta:
        model = FinanceRecord
        fields = "__all__"


class DueForm(forms.ModelForm):
    class Meta:
        model = Due
        fields = "__all__"
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = "__all__"
        widgets = {
            "issued_at": forms.DateInput(attrs={"type": "date"}),
        }
