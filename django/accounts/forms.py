from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に存在します。")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and CustomUser.objects.filter(username=username).exists():
            raise ValidationError("このユーザ名は既に存在します。")
        return username
