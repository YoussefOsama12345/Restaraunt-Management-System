"""
Order database model.

Represents a customer order placed for menu items, including status,
payment details, total amount, and delivery or pickup type.
"""

from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey, Integer, String, Float, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.user import User
from app.db.models.cart import CartItem
from app.db.models.address import Address

import enum

class OrderStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    """
    Represents a placed order by a user.

    Attributes:
        id (int): Primary key of the order.
        user_id (int): The user who placed the order.
        total_amount (float): Total cost of the order.
        status (str): Current status of the order.
        payment_method (str): Payment method (e.g., 'cash', 'credit_card').
        delivery_type (str): Whether it's 'delivery' or 'pickup'.
        address_id (Optional[int]): Delivery address if applicable.
        created_at (datetime): Timestamp of order creation.
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    total_amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[OrderStatusEnum] = mapped_column(SqlEnum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    payment_method: Mapped[str] = mapped_column(String(50), default="cash")
    delivery_type: Mapped[str] = mapped_column(String(50), default="delivery")
    address_id: Mapped[Optional[int]] = mapped_column(ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship('user',back_populates="orders")
    address: Mapped[Optional[Address]] = relationship('address',back_populates="orders")
    cart_items: Mapped[List[CartItem]] = relationship("CartItem", back_populates="order", cascade="all, delete-orphan")
