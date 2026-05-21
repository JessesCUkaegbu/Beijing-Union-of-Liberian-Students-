from django.contrib import admin

from .models import Due, FinanceRecord, Loan


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "record_type", "recorded_at")
    list_filter = ("record_type",)


@admin.register(Due)
class DueAdmin(admin.ModelAdmin):
    list_display = ("student_name", "amount_due", "due_date", "is_paid")
    list_filter = ("is_paid",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("borrower_name", "amount", "issued_at", "is_cleared")
    list_filter = ("is_cleared",)
