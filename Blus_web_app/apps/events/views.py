from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import EventForm
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "events/list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/add.html"
    success_url = reverse_lazy("events:list")
