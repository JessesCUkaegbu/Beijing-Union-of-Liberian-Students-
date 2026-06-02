from django.views.generic import TemplateView


class PostListView(TemplateView):
    template_name = "blog/list.html"


class PostDetailView(TemplateView):
    template_name = "blog/detail.html"


class PostCreateView(TemplateView):
    template_name = "blog/add.html"


class PostUpdateView(TemplateView):
    template_name = "blog/edit.html"
