from django.urls import path

from . import views


app_name = "students"

urlpatterns = [
    # Student member dashboard
    path("student-dashboard/", views.student_dashboard_view, name="student_dashboard"),
    path("profile/", views.student_profile_view, name="profile"),
    # Admin-only student CRUD
    path("", views.student_list_view, name="list"),
    path("add/", views.student_create_view, name="add"),
    path("<int:pk>/", views.student_detail_view, name="detail"),
    path("<int:pk>/edit/", views.student_edit_view, name="edit"),
    path("<int:pk>/delete/", views.student_delete_view, name="delete"),
    # Admin-only inbox of student profile change requests
    path("messages/", views.message_list_view, name="messages"),
    path("messages/<int:pk>/toggle-resolved/", views.message_toggle_resolved_view, name="message_toggle_resolved"),
    path("messages/<int:pk>/delete/", views.message_delete_view, name="message_delete"),
]
