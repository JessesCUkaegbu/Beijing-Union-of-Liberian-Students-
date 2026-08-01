from apps.administration.models import ContactMessage
from apps.students.models import ProfileChangeRequest


def admin_shell_stats(request):
    """Shared context for the admin dashboard shell sidebar (badges, counts)."""
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated or not (user.is_staff or getattr(user, "is_admin", False)):
        return {}
    unresolved_requests = ProfileChangeRequest.objects.filter(is_resolved=False).count()
    unresolved_contacts = ContactMessage.objects.filter(is_resolved=False).count()
    return {
        "message_count": unresolved_requests + unresolved_contacts,
    }
