from django.contrib import admin

from .models import LeadershipMember


@admin.register(LeadershipMember)
class LeadershipMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "position")
