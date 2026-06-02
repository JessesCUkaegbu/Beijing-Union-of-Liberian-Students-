from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class RegisterView(TemplateView):
    template_name = "accounts/register.html"


class ProfileUpdateView(TemplateView):
    template_name = "accounts/register.html"


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
