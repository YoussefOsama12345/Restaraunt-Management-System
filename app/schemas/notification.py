"""
Notification schema definitions.

Defines request and response models for user/admin notifications,
including message content, type, read status, and timestamps.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    """
    Shared fields for notifications.

    Attributes:
        message (str): Main notification text.
        type (str): Notification category (e.g., 'order', 'reservation').
        is_read (bool): Whether the notification has been read.
    """
    message: str = Field(..., example="Your order #1234 has been shipped.")
    type: Optional[str] = Field(default="general", example="order")
    is_read: Optional[bool] = Field(default=False, description="True if the user has viewed the notification")

    model_config = ConfigDict(from_attributes=True)


class NotificationCreate(NotificationBase):
    """Schema for creating a new notification."""
    user_id: int = Field(..., example=1, description="ID of the user receiving the notification")


class NotificationUpdate(BaseModel):
    """
    Schema for updating notification status.

    Attributes:
        is_read (bool): Mark notification as read/unread.
    """
    is_read: bool = Field(..., example=True)

    model_config = ConfigDict(from_attributes=True)


class NotificationRead(NotificationBase):
    """
    Schema for reading notifications from the database.

    Attributes:
        id (int): Notification ID.
        user_id (int): User who received the notification.
        created_at (datetime): When the notification was created.
    """
    id: int
    user_id: int
    created_at: datetime
