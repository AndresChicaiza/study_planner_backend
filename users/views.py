from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.auth import get_user_from_token


# C2 Sprint 3 — Obtener configuración del usuario
@api_view(["GET"])
def get_settings(request):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    return Response({
        "daily_hours_limit": user.daily_hours_limit,
    })


# C2 Sprint 3 — Actualizar límite diario de horas
@api_view(["PATCH"])
def update_settings(request):
    user = get_user_from_token(request)
    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    limit = request.data.get("daily_hours_limit")

    if limit is None:
        return Response(
            {"error": "Debes enviar daily_hours_limit"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        limit = int(limit)
        if limit < 1 or limit > 24:
            raise ValueError
    except (ValueError, TypeError):
        return Response(
            {"error": "El límite debe ser un número entre 1 y 24"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.daily_hours_limit = limit
    user.save()

    return Response({
        "message": "Límite actualizado",
        "daily_hours_limit": user.daily_hours_limit,
    })