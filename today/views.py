from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from core.auth import get_user_from_token

from subtasks.models import Subtask
from conflicts.models import Conflict
from users.models import UserProfile


class TodayView(APIView):

    def get(self, request):

        today = date.today()

        user = get_user_from_token(request)

        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        subtasks = Subtask.objects.filter(
            status="pending",
            activity__user=user
        ).order_by("target_date")

        vencidas = []
        hoy = []
        proximas = []

        total_hours_today = 0

        for s in subtasks:

            if s.target_date < today:
                vencidas.append(s)

            elif s.target_date == today:
                hoy.append(s)
                total_hours_today += s.estimated_hours

            else:
                proximas.append(s)

        # detectar sobrecarga

        overload_detected = False

        if user and total_hours_today > user.daily_hours_limit:

            overload_detected = True

            conflict_exists = Conflict.objects.filter(
                user=user,
                date=today,
                resolved=False
            ).exists()

            if not conflict_exists:
                Conflict.objects.create(
                    user=user,
                    date=today,
                    total_hours=total_hours_today,
                    resolved=False
                )

        def serialize(qs):
            return [
                {
                    "id": x.id,
                    "title": x.title,
                    "date": x.target_date,
                    "hours": x.estimated_hours
                }
                for x in qs
            ]

        return Response({
            "overload": overload_detected,
            "vencidas": serialize(vencidas),
            "hoy": serialize(hoy),
            "proximas": serialize(proximas),
        })