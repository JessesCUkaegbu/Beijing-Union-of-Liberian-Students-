from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/add.html"
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/edit.html"
    success_url = reverse_lazy("blog:list")
