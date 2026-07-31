from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import EventForm
from .models import Event

EVENTS_PER_PAGE = 10


def _is_admin(user):
    return user.is_staff or getattr(user, "is_admin", False)


@login_required
def event_list_view(request):
    """Admin-only, paginated list of all events, reachable from the dashboard sidebar."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")
    paginator = Paginator(Event.objects.all(), EVENTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "events/list.html", {"page_obj": page_obj})


@login_required
def event_create_view(request):
    """Admin-only Add Event form."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    form = EventForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.success(request, f'"{event.title}" was added successfully.')
        return redirect("events:list")

    return render(request, "events/add.html", {"form": form})


@login_required
def event_edit_view(request, pk):
    """Admin-only Edit Event form — reuses the Add Event template/layout."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f'"{event.title}" was updated successfully.')
        return redirect("events:list")

    return render(request, "events/add.html", {"form": form, "event": event})


@login_required
@require_POST
def event_delete_view(request, pk):
    """Admin-only Delete Event action. POST-only so a stray GET can't trigger it."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    event = get_object_or_404(Event, pk=pk)
    title = event.title
    event.delete()
    messages.success(request, f'"{title}" was deleted.')
    return redirect("events:list")


@login_required
def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/detail.html", {"event": event})
