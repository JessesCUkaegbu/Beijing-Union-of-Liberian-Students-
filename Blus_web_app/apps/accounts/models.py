from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager because our User logs in with EMAIL, not username.
    Django's default manager assumes a `username` argument, so we replace it.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        # normalize_email only lowercases the domain. We lowercase the whole
        # address so login is case-insensitive (Stud@X.com == stud@x.com).
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)          # hashes the password — never stored in plain text
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # A normal sign-up: a student, no admin/staff powers.
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", User.Role.STUDENT)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        # Used by `manage.py createsuperuser` — full access + admin role.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model for BLUS.

    We inherit from AbstractUser (so we keep first_name, last_name, is_staff,
    is_active, password handling, and Django's permission system for free),
    but we:
      - remove `username`
      - make `email` the unique login identifier
      - add a `role` to tell admins and students apart.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STUDENT = "student", "Student"

    username = None                                   # we don't use usernames
    email = models.EmailField("email address", unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    USERNAME_FIELD = "email"      # this is what users log in with
    REQUIRED_FIELDS = []          # email + password already required; nothing extra for createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT


class AdminProfile(models.Model):
    """Extra info for users whose role is 'admin' (the BLUS executive/leadership)."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile",
    )
    position = models.CharField(max_length=120, blank=True)   # e.g. President, Treasurer
    phone_number = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} ({self.position or 'Admin'})"
