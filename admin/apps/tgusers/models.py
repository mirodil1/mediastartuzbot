from django.db import models

from apps.core.models import TimeStampedModel


class TelegramUser(TimeStampedModel):
    user_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.user_id})"
    
    class Meta:
        db_table = "tgusers"
