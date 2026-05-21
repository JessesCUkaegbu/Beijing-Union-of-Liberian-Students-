from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} profile"
