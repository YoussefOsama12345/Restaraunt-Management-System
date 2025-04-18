# app/db/models/notification.py

"""
Notification database model.

Stores notifications sent to users or admins, such as order updates,
reminders, and system alerts. Supports read tracking and targeting specific users.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.user import User


class Notification(Base):
    """
    Represents a notification message in the system.

    Attributes:
        id (int): Unique identifier for the notification.
        user_id (Optional[int]): Foreign key to the user who receives the notification.
        title (str): Title or subject of the notification.
        message (str): Full message or content body of the notification.
        is_read (bool): Whether the user has read the notification.
        created_at (datetime): Timestamp of when the notification was created.
        type (Optional[str]): Optional type or category (e.g., 'reminder', 'system', 'alert').
    """

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False, doc="Notification title")
    message: Mapped[str] = mapped_column(Text, nullable=False, doc="Main content of the notification")
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, doc="Has the user read this notification?")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, doc="Time the notification was sent")
    type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, doc="Type of notification (info, warning, etc.)")

    user: Mapped[Optional["User"]] = relationship("User", back_populates="notifications")
