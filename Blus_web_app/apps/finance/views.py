from django.views.generic import TemplateView


class FinanceOverviewView(TemplateView):
    template_name = "finance/overview.html"


class DueListView(TemplateView):
    template_name = "finance/due_list.html"


class LoanListView(TemplateView):
    template_name = "finance/loan_list.html"
