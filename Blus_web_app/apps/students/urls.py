from django.urls import path
from django.views.generic import RedirectView

from .views import DashboardView


app_name = "students"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("", RedirectView.as_view(pattern_name="students:dashboard", permanent=False), name="list"),
    path("add/", RedirectView.as_view(pattern_name="students:dashboard", permanent=False), name="add"),
    path("<int:pk>/", RedirectView.as_view(pattern_name="students:dashboard", permanent=False), name="detail"),
    path("<int:pk>/edit/", RedirectView.as_view(pattern_name="students:dashboard", permanent=False), name="edit"),
]
