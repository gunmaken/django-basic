from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username, deleted_at__isnull=True)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username, deleted_at__isnull=True)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id, deleted_at__isnull=True)
        except UserModel.DoesNotExist:
            return None