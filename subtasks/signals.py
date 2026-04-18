from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Subtask


def recalculate_progress(activity):
    """Recalcula el progreso de una actividad basado en sus subtareas."""
    subtasks = activity.subtasks.all()
    total = subtasks.count()

    if total == 0:
        progress = 0
    else:
        # C2 Sprint 4 — Solo las completadas cuentan para el progreso
        completed = subtasks.filter(completed=True).count()
        progress = int((completed / total) * 100)

    activity.progress = progress
    # Usar update para evitar recursión del signal
    type(activity).objects.filter(pk=activity.pk).update(progress=progress)


@receiver(post_save, sender=Subtask)
def update_progress_on_save(sender, instance, **kwargs):
    recalculate_progress(instance.activity)


@receiver(post_delete, sender=Subtask)
def update_progress_on_delete(sender, instance, **kwargs):
    # Recalcular también cuando se elimina una subtarea
    try:
        recalculate_progress(instance.activity)
    except Exception:
        pass