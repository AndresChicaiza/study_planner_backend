import os
from jose import jwt, JWTError
from users.models import UserProfile


SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")


def get_user_from_token(request):

    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        user_id = payload.get("sub")

        if not user_id:
            return None

        user, _ = UserProfile.objects.get_or_create(supabase_user_id=user_id)
        return user

    except JWTError:
        return None