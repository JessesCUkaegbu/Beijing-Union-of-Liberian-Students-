from django.urls import path

from .views import DueListView, FinanceOverviewView, LoanListView


app_name = "finance"

urlpatterns = [
    path("", FinanceOverviewView.as_view(), name="overview"),
    path("dues/", DueListView.as_view(), name="due_list"),
    path("loans/", LoanListView.as_view(), name="loan_list"),
]
