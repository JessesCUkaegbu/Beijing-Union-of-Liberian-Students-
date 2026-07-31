from django import forms
from django.contrib.auth import get_user_model

from .models import StudentProfile

User = get_user_model()

# Which tab (see add.html) a field belongs to — used by the view to decide
# which tab to show active when validation fails on a re-render.
PERSONAL_FIELDS = {
    "email", "first_name", "last_name", "password1", "password2",
    "student_id", "gender", "date_of_birth", "wechat_id", "phone_number", "image",
}
ACADEMIC_FIELDS = {
    "university", "degree_level", "course", "year_of_study",
    "expected_graduation_year", "sponsorship_status", "residence_area", "housing_type",
}
ENGAGEMENT_FIELDS = {"is_active", "activity_interests", "challenges", "suggestions"}


class StudentForm(forms.Form):
    """
    Admin-facing form that creates/updates BOTH the student's User account
    and their StudentProfile in one step — a student's identity is their
    login account, so "add a student" means provisioning both. Fields mirror
    the BULS Student Survey Google Form so a submitted response can be
    transcribed here directly for safekeeping.
    """

    # ── Account ──────────────────────────────────────────────────────────
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput, required=False)
    student_id = forms.CharField(label="Member/Student ID", max_length=30)

    # ── Personal information ─────────────────────────────────────────────
    gender = forms.ChoiceField(choices=StudentProfile.Gender.choices, widget=forms.RadioSelect, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    wechat_id = forms.CharField(label="WeChat ID", max_length=100, required=False)
    phone_number = forms.CharField(max_length=30, required=False)
    image = forms.ImageField(label="Photo", required=False)

    # ── Academic information ─────────────────────────────────────────────
    university = forms.CharField(label="University name", max_length=150, required=False)
    degree_level = forms.ChoiceField(
        choices=[("", "Select…")] + StudentProfile.DegreeLevel.choices, required=False,
    )
    course = forms.CharField(label="Field of study", max_length=150, required=False)
    year_of_study = forms.ChoiceField(
        choices=[("", "Select…")] + StudentProfile.YearOfStudy.choices, required=False,
    )
    expected_graduation_year = forms.CharField(max_length=9, required=False)
    sponsorship_status = forms.ChoiceField(
        choices=[("", "Select…")] + StudentProfile.SponsorshipStatus.choices, required=False,
    )

    # ── Residence ─────────────────────────────────────────────────────────
    residence_area = forms.CharField(label="District/area of residence in Beijing", max_length=150, required=False)
    housing_type = forms.ChoiceField(
        choices=[("", "Select…")] + StudentProfile.HousingType.choices, required=False,
    )

    # ── BULS engagement ───────────────────────────────────────────────────
    is_active = forms.BooleanField(label="Registered BULS member", required=False, initial=True)
    activity_interests = forms.MultipleChoiceField(
        choices=StudentProfile.ActivityInterest.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    challenges = forms.CharField(
        label="Challenges currently facing as a student in Beijing", widget=forms.Textarea(attrs={"rows": 4}), required=False,
    )
    suggestions = forms.CharField(
        label="Suggestions for improving BULS services", widget=forms.Textarea(attrs={"rows": 4}), required=False,
    )

    def __init__(self, *args, profile=None, **kwargs):
        self.profile = profile  # a StudentProfile instance when editing, else None
        super().__init__(*args, **kwargs)

        if profile:
            self.fields["email"].initial = profile.user.email
            self.fields["first_name"].initial = profile.user.first_name
            self.fields["last_name"].initial = profile.user.last_name
            self.fields["student_id"].initial = profile.student_id
            self.fields["gender"].initial = profile.gender
            self.fields["date_of_birth"].initial = profile.date_of_birth
            self.fields["wechat_id"].initial = profile.wechat_id
            self.fields["phone_number"].initial = profile.phone_number
            self.fields["university"].initial = profile.university
            self.fields["degree_level"].initial = profile.degree_level
            self.fields["course"].initial = profile.course
            self.fields["year_of_study"].initial = profile.year_of_study
            self.fields["expected_graduation_year"].initial = profile.expected_graduation_year
            self.fields["sponsorship_status"].initial = profile.sponsorship_status
            self.fields["residence_area"].initial = profile.residence_area
            self.fields["housing_type"].initial = profile.housing_type
            self.fields["is_active"].initial = profile.is_active
            self.fields["activity_interests"].initial = profile.activity_interests
            self.fields["challenges"].initial = profile.challenges
            self.fields["suggestions"].initial = profile.suggestions

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
                continue
            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("class", "form-input-file")
            else:
                widget.attrs.setdefault("class", "form-input")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email=email)
        if self.profile:
            qs = qs.exclude(pk=self.profile.user_id)
        if qs.exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip()
        qs = StudentProfile.objects.filter(student_id=student_id)
        if self.profile:
            qs = qs.exclude(pk=self.profile.pk)
        if qs.exists():
            raise forms.ValidationError("A student with this ID already exists.")
        return student_id

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Passwords don't match.")
        elif not self.profile:
            self.add_error("password1", "Set a password for this student.")
        return cleaned_data

    def active_tab(self):
        """Which tab to show active — the one containing the first error, if any."""
        error_fields = set(self.errors.keys())
        if error_fields & ACADEMIC_FIELDS:
            return "tab-academic"
        if error_fields & ENGAGEMENT_FIELDS:
            return "tab-engagement"
        return "tab-personal"

    def save(self):
        data = self.cleaned_data

        if self.profile:
            user = self.profile.user
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            if data.get("password1"):
                user.set_password(data["password1"])
            user.save()
            profile = self.profile
        else:
            user = User.objects.create_user(
                email=data["email"],
                password=data["password1"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            profile = StudentProfile(user=user)

        profile.student_id = data["student_id"]
        profile.gender = data["gender"]
        profile.date_of_birth = data["date_of_birth"]
        profile.wechat_id = data["wechat_id"]
        profile.phone_number = data["phone_number"]
        profile.university = data["university"]
        profile.degree_level = data["degree_level"]
        profile.course = data["course"]
        profile.year_of_study = data["year_of_study"]
        profile.expected_graduation_year = data["expected_graduation_year"]
        profile.sponsorship_status = data["sponsorship_status"]
        profile.residence_area = data["residence_area"]
        profile.housing_type = data["housing_type"]
        profile.is_active = data["is_active"]
        profile.activity_interests = data["activity_interests"]
        profile.challenges = data["challenges"]
        profile.suggestions = data["suggestions"]
        if data.get("image"):
            profile.image = data["image"]
        profile.save()
        return profile
