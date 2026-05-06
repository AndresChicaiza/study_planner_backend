from django.db import models
from users.models import UserProfile


class Activity(models.Model):

    TAG_CHOICES = [
        ("tarea", "Tarea"),
        ("examen", "Examen"),
        ("proyecto", "Proyecto"),
        ("lectura", "Lectura"),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    progress = models.IntegerField(default=0)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default="tarea")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title