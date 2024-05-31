from django.contrib.auth.forms import AuthenticationForm
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django import http
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.views.generic import CreateView, DetailView, TemplateView, View, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.password_validation import get_default_password_validators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from typing import Any


class CustomUserCreationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/create_accounts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        password_validators = get_default_password_validators()
        help_texts = []
        for validator in password_validators:
            help_texts.append(validator.get_help_text())

        context["password_help_texts"] = help_texts

        return context

    def form_valid(self, form: BaseModelForm) -> http.HttpResponse:
        # Get the username and password
        user = form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect(reverse("accounts:profile", kwargs={"username": username}))


class CustomSigninView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self) -> str:
        username = self.request.user.username
        return reverse("accounts:profile", kwargs={"username": username})

    def form_invalid(self, form: AuthenticationForm) -> http.HttpResponse:
        form.add_error(
            None, ValidationError("ユーザ名またはパスワードが正しくありません。")
        )
        return redirect(reverse("accounts:signin"))


class CustomSignoutView(LogoutView):
    next_page = reverse_lazy("accounts:hello")


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/detail_account.html"
    model = CustomUser

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        username_or_email = self.kwargs["username"]
        try:
            user = CustomUser.objects.get(username=username_or_email)
        except CustomUser.DoesNotExist:
            user = get_object_or_404(CustomUser, username=username_or_email)
        return user

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        username = self.kwargs["username"]
        context["endpoint_username"] = username
        context["login_username"] = self.request.user.username
        return context


class AccessDeinedView(TemplateView):
    template_name = "accounts/access_deined.html"


class UserAutoCompleteView(View):
    def get(self, request, *args, **kwargs):
        search_word = request.GET.get("term", "")
        users = CustomUser.objects.filter(username__icontains=search_word)
        user_list = list(users.values("username"))
        return http.JsonResponse(user_list, safe=False)


class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ("first_name", "last_name", "birthday", "profile_photo")
    template_name = "accounts/update_user.html"

    def get_success_url(self) -> str:
        username = self.request.user.username
        return reverse("accounts:profile", kwargs={"username": username})

    def get_object(self, *args, **kwargs) -> Model:
        id = self.kwargs["pk"]
        return get_object_or_404(CustomUser, id=id)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["login_username"] = self.request.user.username
        context["endpoint_username"] = self.request.user.username
        return context
