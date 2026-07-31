from django.urls import path

from . import views


app_name = "finance"

urlpatterns = [
    path("", views.FinanceOverviewView.as_view(), name="overview"),
    path("dues/", views.due_list_view, name="due_list"),
    path("dues/add/", views.due_create_view, name="due_add"),
    path("dues/<int:pk>/", views.due_detail_view, name="due_detail"),
    path("dues/<int:pk>/edit/", views.due_edit_view, name="due_edit"),
    path("dues/<int:pk>/delete/", views.due_delete_view, name="due_delete"),
    path("loans/", views.loan_list_view, name="loan_list"),
    path("loans/add/", views.loan_create_view, name="loan_add"),
    path("loans/<int:pk>/", views.loan_detail_view, name="loan_detail"),
    path("loans/<int:pk>/edit/", views.loan_edit_view, name="loan_edit"),
    path("loans/<int:pk>/delete/", views.loan_delete_view, name="loan_delete"),
]
