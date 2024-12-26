from accounts.models import CustomUser
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tasks", default=None
    )

    def __str__(self):
        return self.title
