from django.urls import path

from . import views


app_name = "events"

urlpatterns = [
    path("", views.event_list_view, name="list"),
    path("add/", views.event_create_view, name="add"),
    path("<int:pk>/", views.event_detail_view, name="detail"),
    path("<int:pk>/edit/", views.event_edit_view, name="edit"),
    path("<int:pk>/delete/", views.event_delete_view, name="delete"),
]
