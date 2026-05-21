from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
