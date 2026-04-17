from django.urls import path
from .views import ConflictListView, ResolveConflictView, RedistributeConflictView

urlpatterns = [
    path("", ConflictListView.as_view()),
    path("<int:conflict_id>/resolve/", ResolveConflictView.as_view()),
    path("<int:conflict_id>/redistribute/", RedistributeConflictView.as_view()),
]