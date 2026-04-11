import os
import requests
from jose import jwt, JWTError
from users.models import UserProfile

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        try:
            url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
            res = requests.get(url, timeout=5)
            _jwks_cache = res.json()
        except Exception:
            _jwks_cache = {"keys": []}
    return _jwks_cache


def get_user_from_token(request):
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]

    # Intentar verificar con JWKS (ECC P-256 — sistema nuevo de Supabase)
    try:
        jwks = get_jwks()
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            options={"verify_at_hash": False},
        )
        user_id = payload.get("sub")
        if user_id:
            user, _ = UserProfile.objects.get_or_create(supabase_user_id=user_id)
            return user
    except JWTError:
        pass

    # Fallback: verificar con legacy HS256
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

    return None