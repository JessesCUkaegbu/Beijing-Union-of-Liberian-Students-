from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import StudentForm
from .models import Student


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/list.html"
    context_object_name = "students"


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/detail.html"
    context_object_name = "student"


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/add.html"
    success_url = reverse_lazy("students:list")


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/edit.html"
    success_url = reverse_lazy("students:list")
