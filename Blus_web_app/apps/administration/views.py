from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def dashboard_view(request):
    """
    Admin management dashboard. Login-protected AND admin-only:
    a logged-in student who lands here is bounced to their own dashboard.
    The template still lives in the frontend templates folder.
    """
    if not (request.user.is_staff or getattr(request.user, "is_admin", False)):
        return redirect("students:student_dashboard")
    return render(request, "frontend/admin_dashboard.html")
