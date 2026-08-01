from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.administration.views import about_view, contact_message_create_view, home_view
from apps.blog import views as blog_views
from apps.leadership import views as leadership_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include(("apps.administration.urls", "administration"), namespace="administration")),
    path("accounts/", include("apps.accounts.urls")),
    path("students/", include(("apps.students.urls", "students"), namespace="students")),
    path("events/", include("apps.events.urls")),
    path("finance/", include("apps.finance.urls")),
    path("blog/", include("apps.blog.urls")),
    # Admin-only leadership CRUD. Mounted at /team/ (not /leadership/) since
    # that public path already belongs to the leadership page below.
    path("team/", include(("apps.leadership.urls", "leadership"), namespace="leadership")),

    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("contact/", TemplateView.as_view(template_name="frontend/contact.html"), name="contact"),
    path("contact/submit/", contact_message_create_view, name="contact_submit"),
    path("leadership/", leadership_views.public_leadership_view, name="leadership"),
    path("news/", blog_views.public_blog_list_view, name="blog_public"),
    path("news/<slug:slug>/", blog_views.public_blog_detail_view, name="blog_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
