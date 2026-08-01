from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "is_resolved", "created_at")
    list_filter = ("is_resolved", "subject")
    search_fields = ("first_name", "last_name", "email", "message")
