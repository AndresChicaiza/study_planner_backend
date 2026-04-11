from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subtask


@receiver(post_save, sender=Subtask)
def update_activity_progress(sender, instance, **kwargs):

    activity = instance.activity

    subtasks = activity.subtasks.all()

    total = subtasks.count()
    completed = subtasks.filter(completed=True).count()

    if total == 0:
        progress = 0
    else:
        progress = int((completed / total) * 100)

    activity.progress = progress
    activity.save()