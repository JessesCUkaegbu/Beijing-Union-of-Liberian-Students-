from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LeadershipMemberForm
from .models import LeadershipMember

MEMBERS_PER_PAGE = 10


def _is_admin(user):
    return user.is_staff or getattr(user, "is_admin", False)


# ── Admin dashboard views ───────────────────────────────────────────────────

@login_required
def member_list_view(request):
    """Admin-only, paginated list of all leadership members, reachable from the dashboard sidebar."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")
    paginator = Paginator(LeadershipMember.objects.all(), MEMBERS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "leadership/list.html", {"page_obj": page_obj})


@login_required
def member_create_view(request):
    """Admin-only Add Leadership Member form."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    form = LeadershipMemberForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        member = form.save()
        messages.success(request, f'"{member.name}" was added to the leadership team.')
        return redirect("leadership:list")

    return render(request, "leadership/add.html", {"form": form})


@login_required
def member_edit_view(request, pk):
    """Admin-only Edit Leadership Member form — reuses the Add template/layout."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    member = get_object_or_404(LeadershipMember, pk=pk)
    form = LeadershipMemberForm(request.POST or None, request.FILES or None, instance=member)

    if request.method == "POST" and form.is_valid():
        member = form.save()
        messages.success(request, f'"{member.name}" was updated.')
        return redirect("leadership:list")

    return render(request, "leadership/add.html", {"form": form, "member": member})


@login_required
@require_POST
def member_delete_view(request, pk):
    """Admin-only Delete action. POST-only so a stray GET can't trigger it."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    member = get_object_or_404(LeadershipMember, pk=pk)
    name = member.name
    member.delete()
    messages.success(request, f'"{name}" was removed from the leadership team.')
    return redirect("leadership:list")


@login_required
def member_detail_view(request, pk):
    member = get_object_or_404(LeadershipMember, pk=pk)
    return render(request, "leadership/detail.html", {"member": member})


# ── Public front-end view (leadership/) ─────────────────────────────────────

def public_leadership_view(request):
    """The public /leadership/ page — only ever shows active members."""
    members = LeadershipMember.objects.filter(is_active=True)
    return render(request, "frontend/leadership.html", {"members": members})
