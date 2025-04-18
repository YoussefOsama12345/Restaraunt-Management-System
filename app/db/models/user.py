# app/db/models/user.py

"""
User database model.

Defines user accounts for customers, delivery personnel, and administrators.
Includes fields for authentication, role management, and relationships with
orders, reservations, reviews, addresses, and support tickets.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import String, Integer, Boolean, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.address import Address
from app.db.models.order import Order
from app.db.models.reservation import Reservation
from app.db.models.review import Review
from app.db.models.support_ticket import SupportTicket
from app.db.models.payment import Payment
from app.db.models.cart import CartItem
from app.db.models.delivery_task import DeliveryTask
from app.db.models.notification import Notification

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    DRIVER = "driver"



class User(Base):
    """
    Represents a system user.

    Attributes:
        id (int): Primary key user ID.
        email (str): Unique email used for login.
        hashed_password (str): Encrypted password.
        full_name (str): Optional full name.
        phone_number (str): Optional contact number.
        is_active (bool): Indicates if the user account is active.
        role (UserRole): Role of the user (customer, admin, driver).
        created_at (datetime): User creation timestamp.
        updated_at (datetime): Timestamp of last update.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.CUSTOMER)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    addresses: Mapped[List[Address]] = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders: Mapped[List[Order]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reservations: Mapped[List[Reservation]] = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List[Review]] = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    support_tickets: Mapped[List[SupportTicket]] = relationship("SupportTicket", back_populates="user", cascade="all, delete-orphan")
    payments: Mapped[List[Payment]] = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List[Notification]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    cart_items: Mapped[List[CartItem]] = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    delivery_tasks: Mapped[List[DeliveryTask]] = relationship("DeliveryTask", back_populates="driver", cascade="all, delete-orphan")