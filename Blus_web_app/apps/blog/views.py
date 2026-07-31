from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post

POSTS_PER_PAGE = 10
FRONT_PAGE_POST_LIMIT = 12


def _is_admin(user):
    return user.is_staff or getattr(user, "is_admin", False)


def _apply_publish_action(request, post, was_published):
    """Two submit buttons on the form (name="action") decide publish state."""
    if request.POST.get("action") == "publish":
        post.is_published = True
        if not was_published:
            post.published_at = timezone.now()
    else:
        post.is_published = False


# ── Admin dashboard views ───────────────────────────────────────────────────

@login_required
def post_list_view(request):
    """Admin-only, paginated list of all posts, reachable from the dashboard sidebar."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")
    paginator = Paginator(Post.objects.select_related("author"), POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {"page_obj": page_obj})


@login_required
def post_create_view(request):
    """Admin-only Add Post form, with Publish / Save as draft actions."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        _apply_publish_action(request, post, was_published=False)
        post.save()
        status = "published" if post.is_published else "saved as a draft"
        messages.success(request, f'"{post.title}" was {status}.')
        return redirect("blog:list")

    return render(request, "blog/add.html", {"form": form})


@login_required
def post_edit_view(request, slug):
    """Admin-only Edit Post form — reuses the Add Post template/layout."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    post = get_object_or_404(Post, slug=slug)
    was_published = post.is_published
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        _apply_publish_action(request, post, was_published)
        post.save()
        status = "published" if post.is_published else "saved as a draft"
        messages.success(request, f'"{post.title}" was {status}.')
        return redirect("blog:list")

    return render(request, "blog/add.html", {"form": form, "post": post})


@login_required
@require_POST
def post_delete_view(request, slug):
    """Admin-only Delete Post action. POST-only so a stray GET can't trigger it."""
    if not _is_admin(request.user):
        return redirect("students:student_dashboard")

    post = get_object_or_404(Post, slug=slug)
    title = post.title
    post.delete()
    messages.success(request, f'"{title}" was deleted.')
    return redirect("blog:list")


@login_required
def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/detail.html", {"post": post})


# ── Public front-end views (news/) ──────────────────────────────────────────

def public_blog_list_view(request):
    """The public /news/ page — only ever shows published posts."""
    published = list(Post.objects.select_related("author").filter(is_published=True).order_by("-published_at"))
    featured_post = published[0] if published else None
    posts = published[1:FRONT_PAGE_POST_LIMIT + 1] if published else []
    return render(request, "frontend/blog_public.html", {
        "featured_post": featured_post,
        "posts": posts,
        "total_count": len(published),
    })


def public_blog_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "frontend/blog_detail.html", {"post": post})
