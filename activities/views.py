from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date

from django.db.models import Sum, Count, Q

from .models import Activity
from .serializers import ActivitySerializer
from subtasks.models import Subtask
from core.auth import get_user_from_token


class ActivityListCreateView(APIView):

    def get(self, request):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        activities = Activity.objects.filter(user=user).order_by("-created_at")
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        data = request.data.copy()
        data["user"] = user.id

        serializer = ActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDetailView(APIView):

    def get_object(self, pk, user):
        try:
            return Activity.objects.get(pk=pk, user=user)
        except Activity.DoesNotExist:
            return None

    def patch(self, request, pk):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        activity = self.get_object(pk, user)
        if not activity:
            return Response({"error": "Actividad no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActivitySerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        activity = self.get_object(pk, user)
        if not activity:
            return Response({"error": "Actividad no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        activity.delete()
        return Response({"message": "Actividad eliminada"}, status=status.HTTP_204_NO_CONTENT)


class DashboardView(APIView):

    def get(self, request):
        user = get_user_from_token(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        today = date.today()

        # Una sola consulta SQL con aggregate en lugar de bucles Python
        result = Subtask.objects.filter(activity__user=user).aggregate(
            total_subtasks=Count("id"),
            pending_hours=Sum(
                "estimated_hours",
                filter=Q(status="pending")
            ),
            today_hours=Sum(
                "estimated_hours",
                filter=Q(status="pending", target_date=today)
            ),
        )

        total_activities = Activity.objects.filter(user=user).count()
        pending_hours = result["pending_hours"] or 0
        today_hours = result["today_hours"] or 0
        overload_today = today_hours > user.daily_hours_limit

        return Response({
            "total_activities": total_activities,
            "total_subtasks": result["total_subtasks"] or 0,
            "pending_hours": pending_hours,
            "today_hours": today_hours,
            "overload_today": overload_today,
        })