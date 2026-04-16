from django.urls import path
from .views import get_settings, update_settings

urlpatterns = [
    path("settings/", get_settings),
    path("settings/update/", update_settings),
]