from django.urls import path

from .views import StudentCreateView, StudentDetailView, StudentListView, StudentUpdateView


app_name = "students"

urlpatterns = [
    path("", StudentListView.as_view(), name="list"),
    path("add/", StudentCreateView.as_view(), name="add"),
    path("<int:pk>/", StudentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", StudentUpdateView.as_view(), name="edit"),
]
