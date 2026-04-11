import os
import time
import json
import base64
from users.models import UserProfile


def decode_jwt_payload(token):
    """Decodifica el payload de un JWT sin verificar la firma."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        # Agregar padding si es necesario
        payload_b64 = parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        return json.loads(payload_bytes)
    except Exception:
        return None


def get_user_from_token(request):
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]

    try:
        payload = decode_jwt_payload(token)
        if not payload:
            return None

        # Verificar expiración
        exp = payload.get("exp", 0)
        if exp < time.time():
            return None

        # Verificar audience
        aud = payload.get("aud", "")
        if isinstance(aud, list):
            if "authenticated" not in aud:
                return None
        elif aud != "authenticated":
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        user, _ = UserProfile.objects.get_or_create(supabase_user_id=user_id)
        return user

    except Exception:
        return None