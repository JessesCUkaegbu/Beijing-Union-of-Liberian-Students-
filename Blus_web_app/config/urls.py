from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.blog import views as blog_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include(("apps.administration.urls", "administration"), namespace="administration")),
    path("accounts/", include("apps.accounts.urls")),
    path("students/", include(("apps.students.urls", "students"), namespace="students")),
    path("events/", include("apps.events.urls")),
    path("finance/", include("apps.finance.urls")),
    path("blog/", include("apps.blog.urls")),

    path("", TemplateView.as_view(template_name="frontend/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="frontend/about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="frontend/contact.html"), name="contact"),
    path("leadership/", TemplateView.as_view(template_name="frontend/leadership.html"), name="leadership"),
    path("news/", blog_views.public_blog_list_view, name="blog_public"),
    path("news/<slug:slug>/", blog_views.public_blog_detail_view, name="blog_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
