from rest_framework import serializers
from .models import Subtask


class SubtaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = "__all__"
        read_only_fields = ["completed_at", "created_at"]