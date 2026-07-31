from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import DueForm, LoanForm
from .models import Due, Loan

DUES_PER_PAGE = 10
LOANS_PER_PAGE = 10


def _is_admin(user):
    return user.is_staff or getattr(user, "is_admin", False)


class FinanceOverviewView(TemplateView):
    template_name = "finance/overview.html"


@login_required
def due_list_view(request):
    """Admin-only, paginated list of all dues, reachable from the dashboard sidebar."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")
    paginator = Paginator(Due.objects.select_related("student__user"), DUES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "finance/due_list.html", {"page_obj": page_obj})


@login_required
def due_create_view(request):
    """Admin-only Add Due form."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    form = DueForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        due = form.save()
        messages.success(request, f'"{due.title}" was added for {due.student.full_name}.')
        return redirect("finance:due_list")

    return render(request, "finance/due_add.html", {"form": form})


@login_required
def due_edit_view(request, pk):
    """Admin-only Edit Due form — reuses the Add Due template/layout."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    due = get_object_or_404(Due, pk=pk)
    form = DueForm(request.POST or None, instance=due)

    if request.method == "POST" and form.is_valid():
        due = form.save()
        messages.success(request, f'"{due.title}" was updated.')
        return redirect("finance:due_list")

    return render(request, "finance/due_add.html", {"form": form, "due": due})


@login_required
@require_POST
def due_delete_view(request, pk):
    """Admin-only Delete Due action. POST-only so a stray GET can't trigger it."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    due = get_object_or_404(Due, pk=pk)
    title = due.title
    due.delete()
    messages.success(request, f'"{title}" was deleted.')
    return redirect("finance:due_list")


@login_required
def due_detail_view(request, pk):
    due = get_object_or_404(Due, pk=pk)
    return render(request, "finance/due_detail.html", {"due": due})


@login_required
def loan_list_view(request):
    """Admin-only, paginated list of all loans, reachable from the dashboard sidebar."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")
    paginator = Paginator(Loan.objects.select_related("student__user"), LOANS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "finance/loan_list.html", {"page_obj": page_obj})


@login_required
def loan_create_view(request):
    """Admin-only Add Loan form."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    form = LoanForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        loan = form.save()
        messages.success(request, f'"{loan.purpose}" was added for {loan.student.full_name}.')
        return redirect("finance:loan_list")

    return render(request, "finance/loan_add.html", {"form": form})


@login_required
def loan_edit_view(request, pk):
    """Admin-only Edit Loan form — reuses the Add Loan template/layout."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    loan = get_object_or_404(Loan, pk=pk)
    form = LoanForm(request.POST or None, instance=loan)

    if request.method == "POST" and form.is_valid():
        loan = form.save()
        messages.success(request, f'"{loan.purpose}" was updated.')
        return redirect("finance:loan_list")

    return render(request, "finance/loan_add.html", {"form": form, "loan": loan})


@login_required
@require_POST
def loan_delete_view(request, pk):
    """Admin-only Delete Loan action. POST-only so a stray GET can't trigger it."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    loan = get_object_or_404(Loan, pk=pk)
    purpose = loan.purpose
    loan.delete()
    messages.success(request, f'"{purpose}" was deleted.')
    return redirect("finance:loan_list")


@login_required
def loan_detail_view(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    return render(request, "finance/loan_detail.html", {"loan": loan})
