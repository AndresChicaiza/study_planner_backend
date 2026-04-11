from django.apps import AppConfig


class SubtasksConfig(AppConfig):
    name = 'subtasks'

    def ready(self):
        import subtasks.signals  # noqa: F401