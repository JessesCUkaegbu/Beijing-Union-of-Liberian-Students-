from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

User = get_user_model()


class RegistrationForm(UserCreationForm):
    """
    Public sign-up form. Inherits password1/password2 (with confirmation +
    validation) from UserCreationForm. CSS classes live on the widgets here,
    so templates can render {{ form.field }} and get styled inputs.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply the shared input style to every field (incl. inherited passwords).
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input-field")
        self.fields["email"].widget.attrs["placeholder"] = "you@example.com"
        self.fields["first_name"].widget.attrs["placeholder"] = "Jane"
        self.fields["last_name"].widget.attrs["placeholder"] = "Doe"
        self.fields["password1"].widget.attrs["placeholder"] = "••••••••"
        self.fields["password2"].widget.attrs["placeholder"] = "••••••••"


class LoginForm(AuthenticationForm):
    """
    AuthenticationForm requires a field named `username`, but our USERNAME_FIELD
    is email — so we redefine `username` as a styled email input.
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "input-field",
            "autocomplete": "email",
            "placeholder": "you@example.com",
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # `pr-11` leaves room for the show/password eye button; id `pwd` is the JS hook.
        self.fields["password"].widget.attrs.update({
            "class": "input-field pr-11",
            "autocomplete": "current-password",
            "placeholder": "••••••••",
            "id": "pwd",
        })


# ── Admin-site forms (so Django admin can create/edit our custom user) ──────────
class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "role")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
