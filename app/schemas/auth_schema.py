from pydantic import BaseModel


class Token(BaseModel):
    """Token pair created by AuthService.issue_tokens() (used internally, not sent as-is).

    The handlers split it up: the access token goes in the JSON response body,
    the refresh token goes in an HttpOnly cookie.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenResponse(BaseModel):
    """Response body returned by POST /auth/login and POST /auth/refresh.

    This shape (access_token + token_type) is what the OAuth2 spec expects,
    so tools like Swagger UI can read the token and use it automatically.
    The refresh token is deliberately NOT in here — it's sent as an HttpOnly
    cookie so JavaScript in the browser can never read it.
    """

    # The short-lived signed JWT. The client keeps it in memory and sends it as
    # "Authorization: Bearer <access_token>" on protected requests.
    access_token: str
    # Tells the client how to send the token — always "bearer" here.
    token_type: str = "bearer"
