from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Admin-facing form for creating/editing a blog Post."""

    class Meta:
        model = Post
        fields = ("title", "excerpt", "body", "cover_image")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Annual Cultural Night 2025 Recap"}),
            "excerpt": forms.TextInput(attrs={"placeholder": "Short summary shown on the blog card (optional)"}),
            "body": forms.Textarea(attrs={"rows": 10, "placeholder": "Write the full post…"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "cover_image":
                field.widget.attrs.setdefault("class", "form-input-file")
            else:
                field.widget.attrs.setdefault("class", "form-input")
        self.fields["excerpt"].required = False
        self.fields["cover_image"].required = False
