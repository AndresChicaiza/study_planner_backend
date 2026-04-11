from django.urls import path
from .views import ConflictListView, ResolveConflictView

urlpatterns = [
    path("", ConflictListView.as_view()),
    path("<int:conflict_id>/resolve/", ResolveConflictView.as_view()),
]