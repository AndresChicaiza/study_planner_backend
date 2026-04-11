from django.db import models
from subtasks.models import Subtask

class ProgressLog(models.Model):
    subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)