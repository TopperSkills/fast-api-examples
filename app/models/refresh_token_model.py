# Table that remembers every refresh token we have issued.
# JWTs are "stateless" (valid until they expire, no matter what), so to be able
# to log someone out or block a stolen token we keep a record of each refresh
# token here and check it on every /auth/refresh call.
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # The token's unique id (the "jti" claim). We store the id, not the token
    # itself, so a database leak doesn't hand out usable tokens.
    jti: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    # Which user owns this token. ondelete="CASCADE": deleting a user also
    # deletes their refresh tokens.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # True once the token has been used (rotated) or the user logged out.
    # A revoked token can never be used again.
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
