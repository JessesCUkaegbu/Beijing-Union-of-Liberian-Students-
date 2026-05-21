from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.get_or_create(user=self.object)
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("students:list")

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
