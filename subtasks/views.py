from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Subtask
from .serializers import SubtaskSerializer
from core.auth import get_user_from_token


@api_view(["GET"])
def list_subtasks(request):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    subtasks = Subtask.objects.filter(user=user).order_by("-created_at")
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_subtask(request):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    data = request.data.copy()
    data["user"] = user.id

    serializer = SubtaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# C1 Sprint 4 — Completar con nota y horas reales opcionales
@api_view(["PATCH"])
def complete_subtask(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        subtask = Subtask.objects.get(pk=pk, user=user)
    except Subtask.DoesNotExist:
        return Response({"error": "Subtask no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    subtask.completed = not subtask.completed
    subtask.completed_at = timezone.now() if subtask.completed else None
    subtask.status = "completed" if subtask.completed else "pending"

    # Guardar nota opcional
    note = request.data.get("note", "")
    if note:
        subtask.note = note

    # Guardar horas reales opcionales
    real_hours = request.data.get("real_hours")
    if real_hours is not None:
        try:
            subtask.real_hours = float(real_hours)
        except (ValueError, TypeError):
            pass

    subtask.save()

    return Response({
        "message": "Estado actualizado",
        "completed": subtask.completed,
        "status": subtask.status,
        "note": subtask.note,
        "real_hours": subtask.real_hours,
    })


# C1 Sprint 4 — Posponer subtarea a nueva fecha con nota opcional
@api_view(["PATCH"])
def postpone_subtask(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        subtask = Subtask.objects.get(pk=pk, user=user)
    except Subtask.DoesNotExist:
        return Response({"error": "Subtask no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    new_date = request.data.get("target_date")
    if not new_date:
        return Response(
            {"error": "Debes enviar target_date"},
            status=status.HTTP_400_BAD_REQUEST
        )

    subtask.target_date = new_date
    subtask.status = "postponed"
    subtask.note = request.data.get("note", subtask.note)
    subtask.save()

    return Response({
        "message": "Subtarea pospuesta",
        "target_date": str(subtask.target_date),
        "status": subtask.status,
        "note": subtask.note,
    })


@api_view(["PATCH"])
def update_hours(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        subtask = Subtask.objects.get(pk=pk, user=user)
    except Subtask.DoesNotExist:
        return Response({"error": "Subtask no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if "estimated_hours" in request.data:
        try:
            subtask.estimated_hours = float(request.data["estimated_hours"])
        except (ValueError, TypeError):
            return Response({"error": "Horas estimadas inválidas"}, status=status.HTTP_400_BAD_REQUEST)

    if "real_hours" in request.data:
        try:
            subtask.real_hours = float(request.data["real_hours"])
        except (ValueError, TypeError):
            return Response({"error": "Horas reales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

    subtask.save()
    return Response({
        "message": "Horas actualizadas",
        "estimated_hours": subtask.estimated_hours,
        "real_hours": subtask.real_hours,
    })


@api_view(["PATCH"])
def reschedule_subtask(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        subtask = Subtask.objects.get(pk=pk, user=user)
    except Subtask.DoesNotExist:
        return Response({"error": "Subtask no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    new_date = request.data.get("target_date")
    if not new_date:
        return Response({"error": "Debes enviar target_date"}, status=status.HTTP_400_BAD_REQUEST)

    subtask.target_date = new_date
    subtask.save()

    return Response({
        "message": "Subtarea reprogramada",
        "target_date": str(subtask.target_date),
    })


@api_view(["DELETE"])
def delete_subtask(request, pk):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        subtask = Subtask.objects.get(pk=pk, user=user)
    except Subtask.DoesNotExist:
        return Response({"error": "Subtask no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    subtask.delete()
    return Response({"message": "Subtask eliminada"}, status=status.HTTP_204_NO_CONTENT)