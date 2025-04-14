from django.db import models
from django.contrib.auth.models import User


class Checklist(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(
        "Checklist",
        related_name="checklist_items",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    finished = models.BooleanField(default=False)
