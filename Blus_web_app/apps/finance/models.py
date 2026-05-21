from django.db import models


class FinanceRecord(models.Model):
    RECORD_TYPES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    notes = models.TextField(blank=True)
    recorded_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.record_type})"


class Due(models.Model):
    student_name = models.CharField(max_length=200)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_name} - {self.amount_due}"


class Loan(models.Model):
    borrower_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateField()
    notes = models.TextField(blank=True)
    is_cleared = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower_name} - {self.amount}"
