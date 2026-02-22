from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="telegram")
    chat_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
