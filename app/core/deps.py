# FastAPI dependencies for authentication.
# Any endpoint that adds `current_user = Depends(get_current_user)` becomes a
# protected route: it only runs if the request carries a valid token.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.models.db import get_db
from app.models.user_model import UserModel
from app.services.user_service import UserService

# OAuth2PasswordBearer reads the token from the request header:
#     Authorization: Bearer <token>
# If the header is missing, it automatically responds with 401.
# `tokenUrl` tells Swagger UI (/docs) where to send username/password, which
# enables the "Authorize" button there.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),  # the raw JWT string from the header
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """Turn the Bearer token into the logged-in user, or reject the request with 401."""
    # One shared error for every failure case, so we don't reveal to the
    # client *why* the token was rejected. The WWW-Authenticate header is
    # required by the HTTP spec for 401 responses using Bearer auth.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Verify the signature/expiry and read the payload.
        payload = decode_access_token(token)
        # "sub" holds the user id we put there in create_access_token().
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        # Token is invalid, tampered with, or expired.
        raise credentials_exception

    # A valid token isn't enough: the user might have been deleted since the
    # token was issued, so confirm they still exist in the database.
    user = await UserService.get_one(int(user_id), db)
    if user is None:
        raise credentials_exception
    return user
