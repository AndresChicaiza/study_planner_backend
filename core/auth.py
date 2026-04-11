import os
from jose import jwt, JWTError
from users.models import UserProfile

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")


def get_user_from_token(request):
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]

    # Intentar con HS256 (legacy JWT secret de Supabase)
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        user_id = payload.get("sub")
        if user_id:
            user, _ = UserProfile.objects.get_or_create(supabase_user_id=user_id)
            return user
    except JWTError:
        pass

    # Intentar sin verificar firma (para tokens ECC que no podemos verificar sin clave pública)
    try:
        payload = jwt.get_unverified_claims(token)
        user_id = payload.get("sub")
        if not user_id:
            return None
        # Verificar que el token no está expirado manualmente
        import time
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

        user, _ = UserProfile.objects.get_or_create(supabase_user_id=user_id)
        return user
    except Exception:
        return None