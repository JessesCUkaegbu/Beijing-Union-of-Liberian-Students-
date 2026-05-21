from django.urls import path

from .views import EventCreateView, EventDetailView, EventListView


app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="list"),
    path("add/", EventCreateView.as_view(), name="add"),
    path("<int:pk>/", EventDetailView.as_view(), name="detail"),
]
