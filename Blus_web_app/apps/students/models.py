from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    course = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.FileField(upload_to="students/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("first_name", "last_name")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
