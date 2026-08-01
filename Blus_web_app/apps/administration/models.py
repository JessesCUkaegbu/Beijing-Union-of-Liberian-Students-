from django.db import models


class ContactMessage(models.Model):
    """A message submitted through the public /contact/ page."""

    class Subject(models.TextChoices):
        MEMBERSHIP = "membership", "Membership enquiry"
        EVENTS = "events", "Events & activities"
        SUPPORT = "support", "Student support"
        FINANCE = "finance", "Finance & dues"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=20, choices=Subject.choices, blank=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        status = "resolved" if self.is_resolved else "pending"
        return f"{self.full_name} ({status})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
