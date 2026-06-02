from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "frontend/admin_dashboard.html"
