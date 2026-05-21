from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import Due, FinanceRecord, Loan


class FinanceOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "finance/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = FinanceRecord.objects.all()[:5]
        context["dues_count"] = Due.objects.filter(is_paid=False).count()
        context["loans_count"] = Loan.objects.filter(is_cleared=False).count()
        return context


class DueListView(LoginRequiredMixin, ListView):
    model = Due
    template_name = "finance/due_list.html"
    context_object_name = "dues"


class LoanListView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = "finance/loan_list.html"
    context_object_name = "loans"
