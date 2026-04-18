from django.urls import path
from .views import (
    list_subtasks,
    create_subtask,
    complete_subtask,
    postpone_subtask,
    update_hours,
    reschedule_subtask,
    delete_subtask,
)

urlpatterns = [
    path("", list_subtasks),
    path("create/", create_subtask),
    path("<int:pk>/complete/", complete_subtask),
    path("<int:pk>/postpone/", postpone_subtask),
    path("<int:pk>/hours/", update_hours),
    path("<int:pk>/reschedule/", reschedule_subtask),
    path("<int:pk>/delete/", delete_subtask),
]