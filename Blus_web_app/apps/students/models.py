from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    """
    Role-specific data for users whose role is 'student'.

    Fields mirror the BULS 2026-2027 Academic Year Student Survey (Google
    Form) so admins can transcribe a submitted survey response straight into
    a permanent record here.

    Linked OneToOne to the custom User. We point at settings.AUTH_USER_MODEL
    (not a direct import) — that's the recommended way to reference the user
    model from another app, so this app never hard-depends on accounts.
    """

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class DegreeLevel(models.TextChoices):
        BACHELORS = "bachelors", "Bachelor's"
        MASTERS = "masters", "Master's"
        PHD = "phd", "PhD"
        LANGUAGE = "language", "Language Program"
        OTHER = "other", "Other"

    class YearOfStudy(models.TextChoices):
        FIRST = "first", "First Year"
        SECOND = "second", "Second Year"
        THIRD = "third", "Third Year"
        FOURTH = "fourth", "Fourth Year"
        FIFTH = "fifth", "Fifth Year"
        OTHER = "other", "Other"

    class SponsorshipStatus(models.TextChoices):
        GOV_SCHOLARSHIP = "gov_scholarship", "Government Scholarship"
        CHINESE_GOV_SCHOLARSHIP = "chinese_gov_scholarship", "Chinese Government Scholarship"
        UNIVERSITY_SCHOLARSHIP = "university_scholarship", "University Scholarship"
        SELF_SPONSORED = "self_sponsored", "Self-Sponsored"
        OTHER = "other", "Other"

    class HousingType(models.TextChoices):
        DORMITORY = "dormitory", "Dormitory"
        OFF_CAMPUS = "off_campus", "Off-campus"

    class ActivityInterest(models.TextChoices):
        ACADEMIC = "academic", "Academic Programs"
        SPORTS = "sports", "Sports"
        CULTURAL = "cultural", "Cultural Events"
        CAREER = "career", "Career Development"
        VOLUNTEERING = "volunteering", "Volunteering"
        OTHER = "other", "Other"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    # Internal registry ID — our own record-keeping key, not part of the survey.
    student_id = models.CharField(max_length=30, unique=True)

    # ── Personal information ────────────────────────────────────────────
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    wechat_id = models.CharField("WeChat ID", max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to="students/", null=True, blank=True)

    # ── Academic information ────────────────────────────────────────────
    university = models.CharField("University name", max_length=150, blank=True)
    degree_level = models.CharField(max_length=20, choices=DegreeLevel.choices, blank=True)
    course = models.CharField("Field of study", max_length=150, blank=True)
    year_of_study = models.CharField(max_length=10, choices=YearOfStudy.choices, blank=True)
    expected_graduation_year = models.CharField(max_length=9, blank=True)
    sponsorship_status = models.CharField(max_length=30, choices=SponsorshipStatus.choices, blank=True)

    # ── Residence ────────────────────────────────────────────────────────
    residence_area = models.CharField("District/area of residence in Beijing", max_length=150, blank=True)
    housing_type = models.CharField(max_length=15, choices=HousingType.choices, blank=True)

    # ── BULS engagement ──────────────────────────────────────────────────
    is_active = models.BooleanField("Registered BULS member", default=True)
    activity_interests = models.JSONField(default=list, blank=True)
    challenges = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("student_id",)

    def __str__(self):
        return f"{self.student_id} — {self.full_name}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.email

    @property
    def activity_interests_display(self):
        labels = dict(self.ActivityInterest.choices)
        return [labels.get(value, value) for value in (self.activity_interests or [])]


class ProfileChangeRequest(models.Model):
    """
    A student's request to change their own profile — students can't edit
    their StudentProfile directly, only ask an admin to make the change.
    """

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="change_requests")
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        status = "resolved" if self.is_resolved else "pending"
        return f"Change request from {self.student.full_name} ({status})"
