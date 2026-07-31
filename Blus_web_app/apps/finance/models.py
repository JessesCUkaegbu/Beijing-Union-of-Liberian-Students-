from django.db import models
from django.utils import timezone


class Due(models.Model):
    """A membership/dues payment owed by a student."""

    student = models.ForeignKey(
        "students.StudentProfile",
        on_delete=models.CASCADE,
        related_name="dues",
    )
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(db_index=True)
    is_paid = models.BooleanField(default=False, db_index=True)
    paid_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-due_date",)

    def __str__(self):
        return f"{self.title} — {self.student.full_name}"

    @property
    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.now().date()


class Loan(models.Model):
    """A loan issued to a student, tracked until fully repaid."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        REPAID = "repaid", "Repaid"
        DEFAULTED = "defaulted", "Defaulted"

    student = models.ForeignKey(
        "students.StudentProfile",
        on_delete=models.CASCADE,
        related_name="loans",
    )
    purpose = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_repaid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issued_date = models.DateField(db_index=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-issued_date",)

    def __str__(self):
        return f"{self.purpose} — {self.student.full_name}"

    @property
    def balance_remaining(self):
        return self.amount - self.amount_repaid

    @property
    def is_overdue(self):
        return self.status == self.Status.ACTIVE and bool(self.due_date) and self.due_date < timezone.now().date()
