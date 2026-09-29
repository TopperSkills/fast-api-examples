# Routes for authentication. All paths here start with /auth, and they are
# grouped under the "Auth" section in the Swagger docs (/docs).
from fastapi import APIRouter

from app.handlers.auth_handler import login, logout, refresh
from app.schemas.auth_schema import AccessTokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# POST /auth/login -> body {"access_token": "...", "token_type": "bearer"}
#                     + Set-Cookie: refresh_token=...; HttpOnly
# This path must match `tokenUrl` in OAuth2PasswordBearer (app/core/deps.py).
# `router.post(...)(login)` is the same as decorating `login` with @router.post(...).
router.post("/login", response_model=AccessTokenResponse)(login)

# POST /auth/refresh (no body; reads the refresh_token cookie) -> new access token + new cookie.
router.post("/refresh", response_model=AccessTokenResponse)(refresh)

# POST /auth/logout (no body; reads the refresh_token cookie) -> revokes it and deletes the cookie.
router.post("/logout")(logout)
