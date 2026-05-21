from django.urls import path

from .views import PostCreateView, PostDetailView, PostListView, PostUpdateView


app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("add/", PostCreateView.as_view(), name="add"),
    path("<slug:slug>/", PostDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", PostUpdateView.as_view(), name="edit"),
]
