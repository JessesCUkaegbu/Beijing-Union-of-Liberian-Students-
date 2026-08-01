from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateformat import format as format_date
from django.views.decorators.http import require_POST

from apps.administration.models import ContactMessage
from apps.events.models import Event
from apps.finance.models import Due

from .forms import StudentForm
from .models import ProfileChangeRequest, StudentProfile

STUDENTS_PER_PAGE = 10
UPCOMING_EVENTS_LIMIT = 5
MESSAGES_PER_PAGE = 10


def _is_admin(user):
    return user.is_staff or getattr(user, "is_admin", False)


@login_required
def student_dashboard_view(request):
    """Member dashboard for students after they log in."""
    profile = getattr(request.user, "student_profile", None)

    my_events = Event.objects.filter(event_date__gte=timezone.now().date())[:UPCOMING_EVENTS_LIMIT]

    my_dues = 0
    if profile:
        my_dues = Due.objects.filter(student=profile, is_paid=False).aggregate(total=Sum("amount"))["total"] or 0

    return render(request, "students/student_dashboard.html", {
        "my_dues": my_dues,
        "upcoming_events": my_events.count(),
        "my_events": my_events,
    })


@login_required
def student_profile_view(request):
    """
    Read-only "My Profile" for students — they can see what an admin entered
    for them, but can't edit it directly, only submit a change request.
    """
    if _is_admin(request.user):
        return redirect("administration:dashboard")

    profile = getattr(request.user, "student_profile", None)

    if request.method == "POST":
        if not profile:
            return redirect("students:profile")
        message = request.POST.get("message", "").strip()
        if message:
            ProfileChangeRequest.objects.create(student=profile, message=message)
            messages.success(request, "Your request has been submitted. An admin will review it soon.")
        else:
            messages.error(request, "Please describe what you'd like changed.")
        return redirect("students:profile")

    form = StudentForm(profile=profile, readonly=True) if profile else None
    return render(request, "students/profile.html", {"profile": profile, "form": form})


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


def _profile_request_row(change_request):
    meta = "Resolved" if change_request.is_resolved else "Pending"
    meta += f"|{format_date(change_request.created_at, 'F j, Y g:i A')}"
    return {
        "kind": "profile_request",
        "kind_label": "Profile Request",
        "name": change_request.student.full_name,
        "detail_url": reverse("students:detail", args=[change_request.student.pk]),
        "preview": change_request.message,
        "meta": meta,
        "is_resolved": change_request.is_resolved,
        "created_at": change_request.created_at,
        "toggle_url": reverse("students:message_toggle_resolved", args=[change_request.pk]),
        "delete_url": reverse("students:message_delete", args=[change_request.pk]),
    }


def _contact_message_row(contact_message):
    meta = "Resolved" if contact_message.is_resolved else "Pending"
    meta += f"|{format_date(contact_message.created_at, 'F j, Y g:i A')}"
    meta += f"|{contact_message.email}"
    if contact_message.subject:
        meta += f"|{contact_message.get_subject_display()}"
    return {
        "kind": "contact",
        "kind_label": "Contact Message",
        "name": contact_message.full_name,
        "detail_url": None,
        "preview": contact_message.message,
        "meta": meta,
        "is_resolved": contact_message.is_resolved,
        "created_at": contact_message.created_at,
        "toggle_url": reverse("administration:contact_toggle_resolved", args=[contact_message.pk]),
        "delete_url": reverse("administration:contact_delete", args=[contact_message.pk]),
    }


@login_required
def message_list_view(request):
    """
    Admin-only unified inbox ("Messages" in the sidebar): students' profile
    change requests AND public contact-form submissions, newest first.
    """
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    rows = [
        _profile_request_row(r) for r in ProfileChangeRequest.objects.select_related("student__user")
    ] + [
        _contact_message_row(m) for m in ContactMessage.objects.all()
    ]
    rows.sort(key=lambda row: row["created_at"], reverse=True)

    paginator = Paginator(rows, MESSAGES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "students/message_list.html", {"page_obj": page_obj})


@login_required
@require_POST
def message_toggle_resolved_view(request, pk):
    """Admin-only: flip a change request between pending and resolved."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    change_request = get_object_or_404(ProfileChangeRequest, pk=pk)
    change_request.is_resolved = not change_request.is_resolved
    change_request.save(update_fields=["is_resolved"])
    status = "resolved" if change_request.is_resolved else "reopened"
    messages.success(request, f"Marked the request from {change_request.student.full_name} as {status}.")
    return redirect("students:messages")


@login_required
@require_POST
def message_delete_view(request, pk):
    """Admin-only Delete action. POST-only so a stray GET can't trigger it."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    change_request = get_object_or_404(ProfileChangeRequest, pk=pk)
    student_name = change_request.student.full_name
    change_request.delete()
    messages.success(request, f"Deleted the request from {student_name}.")
    return redirect("students:messages")
