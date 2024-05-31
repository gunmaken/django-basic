from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Todos
from .forms import TodosForm
from accounts.models import CustomUser
from typing import Any


class HelloView(TemplateView):
    template_name = "accounts/hello.html"


class TodosCreateView(LoginRequiredMixin, CreateView):
    model = Todos
    form_class = TodosForm
    template_name = "todos/create_todo.html"

    def get_success_url(self) -> str:
        return reverse(
            "accounts:profile", kwargs={"username": self.request.user.username}
        )

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(f"{self.request.user.username},")
        form.instance.create_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["login_username"] = self.request.user.username
        return context


class TodosListView(ListView):
    model = Todos
    template_name = "todos/todolist.html"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        username = self.kwargs["username"]
        user = CustomUser.objects.get(username=username)
        if user != self.request.user:
            queryset = queryset.filter(is_public=True)
        queryset = queryset.filter(create_user=user).order_by("created_at")
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["endpoint_username"] = self.kwargs["username"]
        return context


class TodoUpdateView(UpdateView):
    model = Todos
    fields = ("title", "description", "deadline", "is_public")
    template_name = "todos/update_todo.html"

    def get_success_url(self) -> str:
        return reverse(
            "accounts:todoslist", kwargs={"username": self.request.user.username}
        )

    def get_object(self, *args, **kwargs) -> Model:
        id = self.kwargs["pk"]
        return get_object_or_404(Todos, id=id)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["login_username"] = self.request.user.username
        context["endpoint_username"] = self.request.user.username
        return context


class TodoDeleteView(DeleteView):
    model = Todos

    def get_success_url(self) -> str:
        return reverse(
            "accounts:todoslist", kwargs={"username": self.request.user.username}
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.kwargs["pk"]
        queryset = queryset.filter(id=id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
