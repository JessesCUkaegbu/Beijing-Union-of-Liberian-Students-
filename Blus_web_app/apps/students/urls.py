from django.urls import path
from django.views.generic import RedirectView

from . import views


app_name = "students"

urlpatterns = [
    # Student member dashboard
    path("student-dashboard/", views.student_dashboard_view, name="student_dashboard"),
    # Student CRUD placeholders (redirect to admin dashboard until built)
    path("", RedirectView.as_view(pattern_name="administration:dashboard", permanent=False), name="list"),
    path("add/", RedirectView.as_view(pattern_name="administration:dashboard", permanent=False), name="add"),
    path("<int:pk>/", RedirectView.as_view(pattern_name="administration:dashboard", permanent=False), name="detail"),
    path("<int:pk>/edit/", RedirectView.as_view(pattern_name="administration:dashboard", permanent=False), name="edit"),
]
