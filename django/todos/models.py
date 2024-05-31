from django.db import models
from accounts.models import CustomUser
import uuid


class Todos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("タイトル", max_length=255, blank=False, null=False)
    description = models.TextField("詳細", blank=True, null=True)
    deadline = models.DateTimeField("締め切り", blank=True, null=True)
    is_public = models.BooleanField("公開", default=False)
    created_at = models.DateTimeField("作成日", editable=False, auto_now_add=True)
    create_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="todos",
        verbose_name="作成者",
    )

    def __str__(self) -> str:
        return self.title
