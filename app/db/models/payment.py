"""
Payment database model.

Tracks payments made by users for their orders, including method, status,
amount, and transaction details from the gateway.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.order import Order
from app.db.models.user import User

import enum

class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Payment(Base):
    """
    Represents a payment transaction associated with an order.

    Attributes:
        id (int): Unique payment identifier.
        order_id (int): The ID of the order the payment is for.
        user_id (int): The user who made the payment.
        amount (float): Total amount paid.
        status (str): Payment status (pending, completed, etc.).
        method (str): Payment method used (e.g., 'stripe', 'cash', 'card').
        transaction_id (str): External gateway transaction ID.
        created_at (datetime): Timestamp when the payment was initiated.
    """

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[PaymentStatusEnum] = mapped_column(SqlEnum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING)
    method: Mapped[str] = mapped_column(String(50), default="cash")
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="payments")
    order: Mapped[Order] = relationship("Order", back_populates="payment")
