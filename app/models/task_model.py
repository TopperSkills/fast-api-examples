# class -> table
from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.db import Base
from typing import Optional


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Board column: "pending" -> "ongoing" -> "completed"
    status: Mapped[str] = mapped_column(String(20), default="pending", server_default="pending", nullable=False)
    # Kept in sync with status (True only when status == "completed")
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Owner of the task. ondelete="CASCADE": deleting a user also deletes their tasks.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
