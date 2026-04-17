from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.auth import get_user_from_token
from .models import Conflict
from subtasks.models import Subtask


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
                "hours": c.total_hours,
                "limit": user.daily_hours_limit,
                "excess": round(c.total_hours - user.daily_hours_limit, 1),
            }
            for c in conflicts
        ]

        return Response(data)


class ResolveConflictView(APIView):

    def patch(self, request, conflict_id):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        conflict = get_object_or_404(Conflict, id=conflict_id, user=user)
        conflict.resolved = True
        conflict.save()

        return Response({"message": "Conflicto resuelto"})


# C4 Sprint 3 — Estrategia: redistribuir subtareas del día con sobrecarga
class RedistributeConflictView(APIView):

    def post(self, request, conflict_id):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        conflict = get_object_or_404(Conflict, id=conflict_id, user=user)

        conflict_date = conflict.date
        limit = user.daily_hours_limit

        # Obtener subtareas del día con sobrecarga ordenadas por horas (mayores primero)
        subtasks_that_day = Subtask.objects.filter(
            user=user,
            target_date=conflict_date,
            status="pending"
        ).order_by("-estimated_hours")

        total = sum(s.estimated_hours for s in subtasks_that_day)

        if total <= limit:
            return Response(
                {"message": "No hay sobrecarga real en ese día"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mover subtareas al día siguiente disponible hasta que las horas queden dentro del límite
        moved = []
        remaining_hours = total
        next_date = conflict_date + timedelta(days=1)

        for subtask in subtasks_that_day:
            if remaining_hours <= limit:
                break

            subtask.target_date = next_date
            subtask.save()
            moved.append({
                "id": subtask.id,
                "title": subtask.title,
                "new_date": str(next_date),
                "hours": subtask.estimated_hours,
            })
            remaining_hours -= subtask.estimated_hours
            # Avanzar al siguiente día si ese también quedaría sobrecargado
            next_date = next_date + timedelta(days=1)

        # Marcar conflicto como resuelto si ya no hay sobrecarga
        if remaining_hours <= limit:
            conflict.resolved = True
            conflict.save()

        return Response({
            "message": f"Se movieron {len(moved)} subtarea(s) a días siguientes",
            "moved": moved,
            "hours_remaining_today": round(remaining_hours, 1),
            "resolved": conflict.resolved,
        })