from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .forms import LoginForm, RegistrationForm


def role_home(user):
    """
    The correct landing page for a user, decided by their REAL role in the DB
    (never by a URL hint — that would be spoofable). Admins/staff go to the
    management dashboard; everyone else (students) goes to the student home.
    """
    if user.is_staff or getattr(user, "is_admin", False):
        return "administration:dashboard"
    return "students:student_dashboard"


def portal_view(request):
    """Chooser landing at /accounts/ — 'Are you an Admin or a Student?'."""
    if request.user.is_authenticated:
        return redirect(role_home(request.user))
    return render(request, "accounts/portal.html")


# Per-portal display copy. Computed in the view so the template stays logic-free.
# (badge, heading, subtitle)
PORTAL_COPY = {
    "admin":   ("Admin Portal",   "Admin sign in",   "Sign in to manage the union."),
    "student": ("Student Portal", "Student sign in", "Sign in to your member account."),
    "":        ("BLUS Portal",    "Welcome back",    "Sign in to your account to continue."),
}


@ratelimit(key="ip", rate="20/5m", method="POST", block=False)
@ratelimit(key="post:username", rate="5/5m", method="POST", block=False)
def login_view(request):
    """Shared email + password login. Heading adapts to the chosen ?as= portal."""
    if request.user.is_authenticated:
        return redirect(role_home(request.user))

    portal = request.GET.get("as", "")          # 'admin' | 'student' | '' (display hint only)
    badge, heading, subtitle = PORTAL_COPY.get(portal, PORTAL_COPY[""])
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and not request.limited and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Welcome back!")
        # Honour ?next= (set by @login_required), else route by real role.
        return redirect(request.GET.get("next") or role_home(user))

    return render(request, "accounts/login.html", {
        "form": form,
        "portal": portal,
        "portal_badge": badge,
        "portal_heading": heading,
        "portal_subtitle": subtitle,
    })


@ratelimit(key="ip", rate="10/h", method="POST", block=False)
@ratelimit(key="post:email", rate="3/h", method="POST", block=False)
def register_view(request):
    """Public sign-up — students only. Admins are provisioned by a superuser."""
    if request.user.is_authenticated:
        return redirect(role_home(request.user))

    form = RegistrationForm(request.POST or None)

    if request.method == "POST":
        if request.limited:
            form.add_error(None, "Too many sign-up attempts from this device. Please try again later.")
        elif form.is_valid():
            form.save()   # hashes password + saves; role defaults to 'student'
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:portal")


@login_required
def profile_view(request):
    """Placeholder so accounts:profile resolves. Real editing comes later."""
    return render(request, "accounts/profile.html")
