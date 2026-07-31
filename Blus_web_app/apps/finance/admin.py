from django.contrib import admin

from .models import Due, Loan


@admin.register(Due)
class DueAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "amount", "due_date", "is_paid")
    list_filter = ("is_paid",)
    search_fields = ("title", "student__student_id", "student__user__email")
    date_hierarchy = "due_date"


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("purpose", "student", "amount", "amount_repaid", "status", "issued_date")
    list_filter = ("status",)
    search_fields = ("purpose", "student__student_id", "student__user__email")
    date_hierarchy = "issued_date"
