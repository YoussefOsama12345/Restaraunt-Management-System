"""
Delivery schema definitions using Pydantic 2.0.

Defines models for creating, updating, and reading delivery tasks,
including assignment to drivers, status tracking, and OTP confirmation.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class DeliveryBase(BaseModel):
    """
    Shared fields for delivery creation and updates.

    Attributes:
        order_id (int): The ID of the order associated with this delivery.
        driver_id (int): The ID of the assigned delivery driver.
        status (str): Current delivery status (e.g., 'assigned', 'en_route', 'delivered').
        otp (str): One-time password used for delivery confirmation.
    """
    order_id: int = Field(..., example=101)
    driver_id: int = Field(..., example=5)
    status: Optional[str] = Field("assigned", example="assigned")
    otp: Optional[str] = Field(None, example="845692")

    model_config = ConfigDict(from_attributes=True)


class DeliveryCreate(DeliveryBase):
    """Schema for creating a new delivery task."""
    pass


class DeliveryUpdateStatus(BaseModel):
    """Schema for updating only the delivery status."""
    status: str = Field(..., example="en_route")


class DeliveryConfirm(BaseModel):
    """Schema for confirming a delivery via OTP."""
    otp: str = Field(..., example="845692")


class DeliveryRead(DeliveryBase):
    """
    Schema for reading delivery task details.

    Attributes:
        id (int): Unique delivery task ID.
        created_at (datetime): Timestamp when the delivery was created.
        updated_at (datetime): Timestamp of the last update.
    """
    id: int
    created_at: datetime
    updated_at: datetime
