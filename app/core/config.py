# Central place for authentication settings.
# Values are read from environment variables (or a .env file) so that secrets
# never have to be hard-coded in the source code.
import os
import secrets
from dotenv import load_dotenv

# Load variables from a .env file (if present) into os.environ.
load_dotenv()

# SECRET_KEY is used to SIGN every JWT token. Anyone who knows this key can
# create valid tokens, so it must be kept private and never committed to git.
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Fallback for local development: generate a random key at startup.
    # Because it changes on every restart, tokens issued before a restart
    # will no longer verify and users must log in again.
    SECRET_KEY = secrets.token_hex(32)
    print(
        "WARNING: SECRET_KEY is not set in the environment. "
        "Using a randomly generated key for this run only — "
        "existing tokens will be invalidated on every restart. "
        "Set SECRET_KEY in a .env file for a stable key."
    )

# HS256 = HMAC with SHA-256: a symmetric algorithm, meaning the same SECRET_KEY
# is used both to sign the token (at login) and to verify it (on each request).
ALGORITHM = "HS256"

# Access token lifetime. Kept SHORT on purpose: access tokens can't be revoked
# (the server doesn't store them), so a stolen one is only useful until it expires.
# When it expires, the client silently gets a new one using the refresh token.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

# Refresh token lifetime. Kept LONG so the user stays logged in for days
# without re-entering their password. These ARE stored in the database, so
# they can be revoked (logout, or when theft is detected).
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Name of the HttpOnly cookie that carries the refresh token.
REFRESH_COOKIE_NAME = "refresh_token"

# Secure cookies are only sent by the browser over HTTPS. Keep this True in
# production; set COOKIE_SECURE=false in .env for local development over plain
# http://127.0.0.1, otherwise the browser will silently drop the cookie.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"

# Frontend origins (scheme + host + port) allowed to call this API from a browser.
# Comma-separated in .env, e.g. CORS_ORIGINS=http://localhost:5173,https://myapp.com
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
