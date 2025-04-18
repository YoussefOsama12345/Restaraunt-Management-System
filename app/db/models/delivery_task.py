# app/db/models/delivery_task.py

"""
DeliveryTask database model.

Tracks delivery assignments for orders handled by drivers.
Includes status updates and optional OTP confirmation for secure delivery completion.
"""

from sqlalchemy import ForeignKey, String, Integer, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
import enum


class DeliveryStatus(str, enum.Enum):
    """Enumeration of valid delivery statuses."""
    ASSIGNED = "assigned"
    EN_ROUTE = "en_route"
    DELIVERED = "delivered"
    FAILED = "failed"


class DeliveryTask(Base):
    """
    Represents a delivery assignment for an order.

    Attributes:
        id (int): Unique task ID.
        order_id (int): Linked order being delivered.
        driver_id (int): Delivery user (driver) assigned to this task.
        status (str): Current status of the delivery (e.g., assigned, delivered).
        otp_code (str): Optional code required for delivery confirmation.
        confirmed (bool): Indicates if delivery has been confirmed.
    """

    __tablename__ = "delivery_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus), default=DeliveryStatus.ASSIGNED)
    otp_code: Mapped[str] = mapped_column(String(10), nullable=True, doc="OTP code for confirmation")
    confirmed: Mapped[bool] = mapped_column(default=False, doc="Whether delivery has been confirmed")

    
    driver = relationship("User", back_populates="delivery_tasks")
    order = relationship("Order", back_populates="delivery_task")
