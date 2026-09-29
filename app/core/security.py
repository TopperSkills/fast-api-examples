# Low-level security helpers used by the rest of the app:
#   1. Password hashing   -> so plain-text passwords are never stored in the database.
#   2. JWT token handling -> so a logged-in user can prove who they are on later requests.
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    """Turn a plain-text password into a bcrypt hash for storing in the database.

    bcrypt.gensalt() creates a random "salt", so the same password produces a
    different hash each time. The salt is stored inside the hash string itself,
    which is why verify_password() doesn't need it passed separately.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login password against the stored hash.

    Hashes are one-way (they can't be decrypted), so bcrypt re-hashes the given
    password with the salt from the stored hash and compares the results.
    """
    print(f"pass: ",plain_password)
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Create a signed JWT that identifies the user.

    The payload ("claims") holds:
      - "sub" (subject): who the token belongs to — here, the user's id.
      - "exp" (expiry):  when the token stops being valid.
    The payload is only base64-encoded, NOT encrypted, so never put secrets
    (like passwords) in it. The signature is what stops it being tampered with.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    # "type" marks this as an access token, so it can't be used as a refresh token (and vice versa).
    payload = {"sub": subject, "type": "access", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str, jti: str, expires_at: datetime) -> str:
    """Create a signed, long-lived JWT used only to get new access tokens.

    "jti" (JWT ID) is a unique id for this token. The same id is saved in the
    refresh_tokens table, which lets the server revoke this specific token
    later — something a plain JWT can't do on its own.
    """
    payload = {"sub": subject, "type": "refresh", "jti": jti, "exp": expires_at}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str, expected_type: str) -> dict:
    """Verify a JWT and return its payload.

    jwt.decode() checks the signature with SECRET_KEY and also checks "exp".
    If the token was modified, signed with another key, or has expired, it
    raises a PyJWTError (handled by the callers).
    Passing `algorithms=[...]` explicitly prevents attackers from choosing a
    weaker algorithm in the token header.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # Both token kinds are signed with the same key, so the signature alone
    # can't tell them apart — check the "type" claim we added ourselves.
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"Expected a {expected_type} token")
    return payload


def decode_access_token(token: str) -> dict:
    """Verify an access token (used by get_current_user in app/core/deps.py)."""
    return _decode_token(token, "access")


def decode_refresh_token(token: str) -> dict:
    """Verify a refresh token (used by /auth/refresh and /auth/logout)."""
    return _decode_token(token, "refresh")
