from django.db import models

class UserProfile(models.Model):
    supabase_user_id = models.CharField(max_length=255, unique=True)
    daily_hours_limit = models.IntegerField(default=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supabase_user_id