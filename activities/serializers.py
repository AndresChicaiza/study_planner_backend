from rest_framework import serializers
from .models import Activity
from subtasks.models import Subtask

class SubtaskInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    subtasks = SubtaskInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = "__all__"