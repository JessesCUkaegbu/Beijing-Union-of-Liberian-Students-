from django.db import models


class LeadershipMember(models.Model):
    """A BLUS executive/board member shown on the public Leadership page."""

    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="leadership/", null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField(
        "Show on public site", default=True,
        help_text="Uncheck to hide from the public leadership page without deleting.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return f"{self.name} — {self.position}"

    @property
    def initials(self):
        parts = self.name.split()
        return "".join(part[0] for part in parts[:2]).upper() if parts else "?"
