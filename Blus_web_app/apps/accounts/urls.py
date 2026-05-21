from django.urls import path

from .views import CustomLoginView, ProfileUpdateView, RegisterView, logout_view


app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("logout/", logout_view, name="logout"),
]
