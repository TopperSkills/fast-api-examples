# Request handlers for the auth endpoints:
#   POST /auth/login   -> email + password -> access token (JSON) + refresh token (HttpOnly cookie)
#   POST /auth/refresh -> refresh cookie   -> NEW access token (JSON) + NEW refresh cookie
#   POST /auth/logout  -> refresh cookie   -> refresh token is revoked, cookie is deleted
# The client sends the access token in the Authorization header on protected
# requests. When it expires (401), the client calls /auth/refresh instead of
# asking the user for their password again. The browser attaches the refresh
# cookie automatically — the frontend code never sees or touches it.
from fastapi import Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import COOKIE_SECURE, REFRESH_COOKIE_NAME, REFRESH_TOKEN_EXPIRE_DAYS
from app.models.db import get_db
from app.schemas.auth_schema import AccessTokenResponse
from app.services.auth_service import AuthService

# The cookie is only sent by the browser to paths under /auth, so it isn't
# attached to every other API request (like /users).
REFRESH_COOKIE_PATH = "/auth"


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Attach the refresh token to the response as an HttpOnly cookie."""
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        # HttpOnly: JavaScript (document.cookie) can't read it, so an XSS
        # attack can't steal it. The browser still sends it automatically.
        httponly=True,
        # Secure: only sent over HTTPS (see COOKIE_SECURE in app/core/config.py).
        secure=COOKIE_SECURE,
        # SameSite=Strict: not sent on requests started by other websites,
        # which protects /auth/refresh and /auth/logout against CSRF.
        samesite="strict",
        path=REFRESH_COOKIE_PATH,
        # Lifetime in seconds; matches the refresh token's own expiry.
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


async def login(
    # FastAPI gives us this Response object so we can add headers/cookies to
    # the response it builds from our return value.
    response: Response,
    # OAuth2PasswordRequestForm reads the body as FORM data (not JSON), with
    # fields named `username` and `password` — this is what the OAuth2 spec
    # requires and what Swagger UI's "Authorize" button sends.
    # We use the `username` field to carry the user's email.
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> AccessTokenResponse:
    # Check the email/password against the database.
    user = await AuthService.authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        # Deliberately vague message: don't say whether the email or the
        # password was wrong, so attackers can't discover which emails exist.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Credentials are correct: issue an access token + refresh token for this user.
    tokens = await AuthService.issue_tokens(user.id, db)
    # Refresh token -> HttpOnly cookie; access token -> JSON body.
    _set_refresh_cookie(response, tokens.refresh_token)
    return AccessTokenResponse(access_token=tokens.access_token)


async def refresh(
    response: Response,
    # Cookie(alias=...) reads the cookie named "refresh_token" from the request.
    # It's None if the browser didn't send one (e.g. the user never logged in).
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
    db: AsyncSession = Depends(get_db),
) -> AccessTokenResponse:
    # No password needed here — the refresh token itself proves the user logged in earlier.
    tokens = await AuthService.rotate_refresh_token(refresh_token, db) if refresh_token else None
    if tokens is None:
        # Missing, invalid, expired, revoked or reused: the client must log in again.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Rotation: the old refresh token is now revoked, so overwrite the cookie
    # with the new one (same name + path replaces it in the browser).
    _set_refresh_cookie(response, tokens.refresh_token)
    return AccessTokenResponse(access_token=tokens.access_token)


async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
    db: AsyncSession = Depends(get_db),
):
    if refresh_token:
        await AuthService.revoke_refresh_token(refresh_token, db)
    # Tell the browser to remove the cookie. Path must match the one used when setting it.
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="strict",
    )
    return {"message": "Logged out"}
