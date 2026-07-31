from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    """A BLUS blog post. Drafts are admin-only; published posts show on /news/."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short summary shown on the blog card. Falls back to the start of the post body.",
    )
    body = models.TextField()
    cover_image = models.ImageField(upload_to="blog/", null=True, blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or "post"
            slug = base_slug
            suffix = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                suffix += 1
                slug = f"{base_slug}-{suffix}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def summary(self):
        if self.excerpt:
            return self.excerpt
        text = self.body.strip()
        return (text[:160] + "…") if len(text) > 160 else text
