from apps.blog.models import Post
from apps.events.models import Event


def admin_shell_stats(request):
    if not request.user.is_authenticated:
        return {}

    return {
        "notification_count": Event.objects.filter(is_published=True).count(),
        "message_count": Post.objects.filter(is_published=True).count(),
    }
