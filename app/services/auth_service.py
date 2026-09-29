# Business logic for authentication (kept separate from the HTTP layer in
# app/handlers/auth_handler.py so it can be reused and tested on its own).
import uuid
from datetime import datetime, timedelta, timezone

from jwt import PyJWTError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.models.refresh_token_model import RefreshTokenModel
from app.models.user_model import UserModel
from app.schemas.auth_schema import Token


class AuthService:
    @staticmethod
    async def authenticate_user(email: str, password: str, db: AsyncSession) -> UserModel | None:
        """Return the user if the email/password are correct, otherwise None."""
        # Normalise the email (trim spaces, lower-case) so "Bob@Mail.com " and
        # "bob@mail.com" are treated as the same login.
        result = await db.execute(select(UserModel).where(UserModel.email == email.strip().lower()))
        user = result.scalar_one_or_none()
        # Fail if the user doesn't exist OR the password doesn't match the
        # stored bcrypt hash. Both cases return None so the caller can't tell
        # them apart (and neither can an attacker).
        if user is None or not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    async def issue_tokens(user_id: int, db: AsyncSession) -> Token:
        """Create a new access + refresh token pair and record the refresh token in the database."""
        # A random, unique id for the refresh token.
        jti = uuid.uuid4().hex
        expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        db.add(RefreshTokenModel(jti=jti, user_id=user_id, expires_at=expires_at))
        await db.commit()
        # JWT claims should be strings, hence str(user_id).
        return Token(
            access_token=create_access_token(subject=str(user_id)),
            refresh_token=create_refresh_token(subject=str(user_id), jti=jti, expires_at=expires_at),
        )

    @staticmethod
    async def rotate_refresh_token(refresh_token: str, db: AsyncSession) -> Token | None:
        """Swap a valid refresh token for a brand-new token pair ("rotation").

        Every refresh token works only ONCE: using it revokes it and issues a
        new one. Returns None if the token is invalid, expired, unknown or
        already used.
        """
        try:
            # Checks the signature, the expiry, and that it's a "refresh" token.
            payload = decode_refresh_token(refresh_token)
        except PyJWTError:
            return None

        # Look up the database record. with_for_update() locks the row so two
        # simultaneous requests with the same token can't both succeed.
        result = await db.execute(
            select(RefreshTokenModel)
            .where(RefreshTokenModel.jti == payload.get("jti"))
            .with_for_update()
        )
        stored = result.scalar_one_or_none()
        if stored is None:
            # Unknown token, or its user was deleted (rows are cascade-deleted).
            return None

        if stored.revoked:
            # REUSE DETECTED: this token was already used once. The real user
            # only ever holds the newest token, so an old one showing up means
            # someone copied it. We can't tell who is the attacker, so to be
            # safe we revoke ALL of this user's refresh tokens — everyone has
            # to log in again with the password.
            await db.execute(
                update(RefreshTokenModel)
                .where(RefreshTokenModel.user_id == stored.user_id)
                .values(revoked=True)
            )
            await db.commit()
            return None

        # Normal case: mark the old token as used, then hand out a new pair
        # (issue_tokens commits both changes together).
        stored.revoked = True
        return await AuthService.issue_tokens(stored.user_id, db)

    @staticmethod
    async def revoke_refresh_token(refresh_token: str, db: AsyncSession) -> None:
        """Log out: revoke the given refresh token so it can't be used again.

        Note: the current access token keeps working until it expires (at most
        ACCESS_TOKEN_EXPIRE_MINUTES) — that's why access tokens are short-lived.
        The client should simply delete both tokens on logout.
        """
        try:
            payload = decode_refresh_token(refresh_token)
        except PyJWTError:
            # Invalid token: nothing to revoke. Logout still "succeeds".
            return
        await db.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.jti == payload.get("jti"))
            .values(revoked=True)
        )
        await db.commit()
