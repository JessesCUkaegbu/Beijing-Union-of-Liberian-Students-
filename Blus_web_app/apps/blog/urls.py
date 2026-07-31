from django.urls import path

from . import views


app_name = "blog"

urlpatterns = [
    path("", views.post_list_view, name="list"),
    path("add/", views.post_create_view, name="add"),
    path("<slug:slug>/", views.post_detail_view, name="detail"),
    path("<slug:slug>/edit/", views.post_edit_view, name="edit"),
    path("<slug:slug>/delete/", views.post_delete_view, name="delete"),
]
