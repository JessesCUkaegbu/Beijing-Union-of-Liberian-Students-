from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "full_name", "email", "course", "is_active")
    list_filter = ("is_active", "course")
    search_fields = ("first_name", "last_name", "student_id", "email")
