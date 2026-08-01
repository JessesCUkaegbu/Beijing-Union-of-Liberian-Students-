from django.urls import path

from . import views


app_name = "administration"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("contact-messages/<int:pk>/toggle-resolved/", views.contact_toggle_resolved_view, name="contact_toggle_resolved"),
    path("contact-messages/<int:pk>/delete/", views.contact_delete_view, name="contact_delete"),
]
