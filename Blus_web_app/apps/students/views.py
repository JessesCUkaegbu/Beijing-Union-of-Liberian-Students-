from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import StudentForm
from .models import StudentProfile

STUDENTS_PER_PAGE = 10


def _is_admin(user):
    return user.is_staff or getattr(user, "is_admin", False)


@login_required
def student_dashboard_view(request):
    """Member dashboard for students after they log in."""
    return render(request, "students/student_dashboard.html")


@login_required
def student_list_view(request):
    """Admin-only, paginated list of all students, reachable from the dashboard sidebar."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")
    paginator = Paginator(StudentProfile.objects.select_related("user"), STUDENTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "students/list.html", {"page_obj": page_obj})


@login_required
def student_create_view(request):
    """Admin-only Add Student form — provisions both the User and the StudentProfile."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    form = StudentForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        profile = form.save()
        messages.success(request, f'"{profile.full_name}" was added successfully.')
        return redirect("students:list")

    return render(request, "students/add.html", {"form": form, "active_tab": form.active_tab()})


@login_required
def student_edit_view(request, pk):
    """Admin-only Edit Student form — reuses the Add Student template/layout."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    profile = get_object_or_404(StudentProfile, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, profile=profile)

    if request.method == "POST" and form.is_valid():
        profile = form.save()
        messages.success(request, f'"{profile.full_name}" was updated successfully.')
        return redirect("students:list")

    return render(request, "students/add.html", {
        "form": form, "profile": profile, "active_tab": form.active_tab(),
    })


@login_required
@require_POST
def student_delete_view(request, pk):
    """Admin-only Delete Student action. Removes the whole account (login + profile)."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    profile = get_object_or_404(StudentProfile, pk=pk)
    name = profile.full_name
    profile.user.delete()  # cascades to the StudentProfile
    messages.success(request, f'"{name}" was deleted.')
    return redirect("students:list")


@login_required
def student_detail_view(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    return render(request, "students/detail.html", {"profile": profile})
