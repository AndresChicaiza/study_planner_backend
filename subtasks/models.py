from django.db import models
from activities.models import Activity
from users.models import UserProfile


class Subtask(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En progreso"),
        ("completed", "Completada"),
        ("postponed", "Pospuesta"),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="subtasks")

    title = models.CharField(max_length=255)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    target_date = models.DateField(null=True, blank=True)

    estimated_hours = models.FloatField(default=1)
    real_hours = models.FloatField(default=0)

    # C1 Sprint 4 — nota opcional al registrar avance
    note = models.TextField(blank=True, default="")

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title