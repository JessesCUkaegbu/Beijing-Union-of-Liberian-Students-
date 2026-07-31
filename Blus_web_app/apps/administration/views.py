from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.blog.models import Post
from apps.events.models import Event
from apps.finance.models import Due, Loan
from apps.students.models import StudentProfile


def _month_start(date):
    return date.replace(day=1)


def _add_months(date, months):
    month_index = date.month - 1 + months
    year = date.year + month_index // 12
    month = month_index % 12 + 1
    return date.replace(year=year, month=month, day=1)


def _growth_pct(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return round((current - previous) / previous * 100)


def _new_students_chart(this_month_start):
    """12 monthly bars of new-student sign-ups, most recent month last.

    One grouped query (TruncMonth + Count) instead of one .count() per month.
    """
    window_start = _add_months(this_month_start, -11)
    monthly_rows = (
        StudentProfile.objects
        .filter(created_at__date__gte=window_start)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
    )
    counts_by_month = {row["month"].date(): row["count"] for row in monthly_rows}

    month_labels = []
    counts = []
    month_cursor = window_start
    for _ in range(12):
        counts.append(counts_by_month.get(month_cursor, 0))
        month_labels.append(month_cursor.strftime("%b"))
        month_cursor = _add_months(month_cursor, 1)

    max_count = max(counts) or 1
    bar_width = 560 / 12
    chart_data = []
    for i, count in enumerate(counts):
        bar_h = max(8, round((count / max_count) * 110)) if count else 8
        chart_data.append({
            "bar_x": round(i * bar_width + (bar_width - 28) / 2, 1),
            "bar_y": 130 - bar_h,
            "bar_h": bar_h,
            "highlight": i == 11,
        })
    return chart_data, month_labels


@login_required
def dashboard_view(request):
    """
    Admin management dashboard. Login-protected AND admin-only:
    a logged-in student who lands here is bounced to their own dashboard.
    The template still lives in the frontend templates folder.
    """
    if not (request.user.is_staff or getattr(request.user, "is_admin", False)):
        return redirect("students:student_dashboard")

    today = timezone.now().date()
    this_month_start = _month_start(today)
    last_month_start = _add_months(this_month_start, -1)
    this_month = Q(created_at__date__gte=this_month_start)
    last_month = Q(created_at__date__gte=last_month_start, created_at__date__lt=this_month_start)

    # ── Students (1 query) ──────────────────────────────────────────────
    student_stats = StudentProfile.objects.aggregate(
        total=Count("id"),
        this_month=Count("id", filter=this_month),
        last_month=Count("id", filter=last_month),
    )
    total_students = student_stats["total"]
    student_growth = _growth_pct(student_stats["this_month"], student_stats["last_month"])

    # ── Events (1 query) ─────────────────────────────────────────────────
    event_stats = Event.objects.aggregate(
        active=Count("id", filter=Q(event_date__gte=today)),
        this_month=Count("id", filter=this_month),
        last_month=Count("id", filter=last_month),
    )
    active_events = event_stats["active"]
    event_growth = _growth_pct(event_stats["this_month"], event_stats["last_month"])

    # ── Dues (1 query) ───────────────────────────────────────────────────
    due_stats = Due.objects.aggregate(
        total_paid=Sum("amount", filter=Q(is_paid=True)),
        this_month_paid=Sum("amount", filter=Q(is_paid=True, paid_date__gte=this_month_start)),
        last_month_paid=Sum("amount", filter=Q(
            is_paid=True, paid_date__gte=last_month_start, paid_date__lt=this_month_start,
        )),
        pending=Count("id", filter=Q(is_paid=False)),
        overdue=Count("id", filter=Q(is_paid=False, due_date__lt=today)),
    )
    dues_collected = due_stats["total_paid"] or 0
    dues_growth = _growth_pct(due_stats["this_month_paid"] or 0, due_stats["last_month_paid"] or 0)
    pending_dues = due_stats["pending"]
    overdue_count = due_stats["overdue"]

    # ── Loans (1 query) ──────────────────────────────────────────────────
    loan_totals = Loan.objects.exclude(status=Loan.Status.REPAID).aggregate(
        total_amount=Sum("amount"), total_repaid=Sum("amount_repaid"),
    )
    outstanding_loans = (loan_totals["total_amount"] or 0) - (loan_totals["total_repaid"] or 0)

    # ── Blog (1 query) ───────────────────────────────────────────────────
    published_posts = Post.objects.filter(is_published=True).count()

    # ── Finance summary + growth chart ──────────────────────────────────
    total_finance = dues_collected
    chart_data, month_labels = _new_students_chart(this_month_start)

    recent_students = StudentProfile.objects.select_related("user").order_by("-created_at")[:8]

    return render(request, "frontend/admin_dashboard.html", {
        "total_students": total_students,
        "student_growth": student_growth,
        "active_events": active_events,
        "event_growth": event_growth,
        "dues_collected": dues_collected,
        "dues_growth": dues_growth,
        "pending_dues": pending_dues,
        "overdue_count": overdue_count,
        "chart_data": chart_data,
        "month_labels": month_labels,
        "total_finance": total_finance,
        "outstanding_loans": outstanding_loans,
        "event_spending": 0,  # no expense-tracking model yet
        "published_posts": published_posts,
        "recent_students": recent_students,
        "recent_students_count": len(recent_students),
    })
