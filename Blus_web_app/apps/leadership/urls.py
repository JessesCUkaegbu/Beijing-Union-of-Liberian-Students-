from django.urls import path

from . import views


app_name = "leadership"

urlpatterns = [
    path("", views.member_list_view, name="list"),
    path("add/", views.member_create_view, name="add"),
    path("<int:pk>/", views.member_detail_view, name="detail"),
    path("<int:pk>/edit/", views.member_edit_view, name="edit"),
    path("<int:pk>/delete/", views.member_delete_view, name="delete"),
]
