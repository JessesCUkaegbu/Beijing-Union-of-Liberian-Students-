from django.views.generic import TemplateView


class EventListView(TemplateView):
    template_name = "events/list.html"


class EventDetailView(TemplateView):
    template_name = "events/detail.html"


class EventCreateView(TemplateView):
    template_name = "events/add.html"
