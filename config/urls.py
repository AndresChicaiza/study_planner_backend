from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from activities.views import ActivityListCreateView, ActivityDetailView, DashboardView
from today.views import TodayView


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health),

    # Actividades
    path('api/activities/', ActivityListCreateView.as_view()),
    path('api/activities/<int:pk>/', ActivityDetailView.as_view()),

    # Subtasks
    path('api/subtasks/', include('subtasks.urls')),

    # Usuarios — configuración
    path('api/users/', include('users.urls')),

    # Dashboard y hoy
    path('api/dashboard/', DashboardView.as_view()),
    path('api/today/', TodayView.as_view()),

    # Conflictos
    path('api/conflicts/', include('conflicts.urls')),
]