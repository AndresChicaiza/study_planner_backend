from rest_framework.views import APIView
from rest_framework.response import Response
from core.auth import get_user_from_token
from .models import Conflict
from django.shortcuts import get_object_or_404
from rest_framework import status


class ConflictListView(APIView):

    def get(self, request):

        user = get_user_from_token(request)

        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        conflicts = Conflict.objects.filter(
            user=user,
            resolved=False
        ).order_by("date")

        data = [
            {
                "id": c.id,
                "date": c.date,
                "hours": c.total_hours
            }
            for c in conflicts
        ]

        return Response(data)

class ResolveConflictView(APIView):

    def patch(self, request, conflict_id):
        user = get_user_from_token(request)

        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        conflict = get_object_or_404(
            Conflict,
            id=conflict_id,
            user=user
        )

        conflict.resolved = True
        conflict.save()

        return Response({"message": "Conflict resolved"})