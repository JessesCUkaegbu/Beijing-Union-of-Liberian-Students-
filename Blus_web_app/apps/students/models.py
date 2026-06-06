from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    """
    Role-specific data for users whose role is 'student'.

    Linked OneToOne to the custom User. We point at settings.AUTH_USER_MODEL
    (not a direct import) — that's the recommended way to reference the user
    model from another app, so this app never hard-depends on accounts.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    student_id = models.CharField(max_length=30, unique=True)
    university = models.CharField(max_length=150, blank=True)
    course = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to="students/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("student_id",)

    def __str__(self):
        return f"{self.student_id} — {self.user.get_full_name() or self.user.email}"
