from django.contrib import admin

from .models import ProfileChangeRequest, StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student_id", "user", "university", "course", "is_active")
    list_filter = ("is_active", "university")
    search_fields = ("student_id", "user__email", "user__first_name", "user__last_name")


@admin.register(ProfileChangeRequest)
class ProfileChangeRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "is_resolved", "created_at")
    list_filter = ("is_resolved",)
    search_fields = ("student__student_id", "student__user__email", "message")
