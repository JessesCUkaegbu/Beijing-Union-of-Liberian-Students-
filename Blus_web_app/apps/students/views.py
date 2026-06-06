from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def student_dashboard_view(request):
    """Member dashboard for students after they log in."""
    return render(request, "students/student_dashboard.html")
