from django.db import models
from users.models import UserProfile

class Conflict(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField()
    total_hours = models.IntegerField()
    resolved = models.BooleanField(default=False)