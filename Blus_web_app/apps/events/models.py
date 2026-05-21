from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("event_date",)

    def __str__(self):
        return self.title
