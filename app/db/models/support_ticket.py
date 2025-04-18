# app/db/models/support_ticket.py

"""
SupportTicket database model.

Handles customer support messages, including inquiries about orders,
reservations, or general issues. Tracks ticket status and conversation.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Text, ForeignKey,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.user import User
from app.db.models.order import Order
from app.db.models.reservation import Reservation


class TicketStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SupportTicket(Base):
    """
    Represents a customer support ticket.

    Attributes:
        id (int): Primary key identifier.
        user_id (int): Foreign key to the user who submitted the ticket.
        subject (str): Short title or issue summary.
        message (str): Main content or message body.
        order_id (int): Optional related order.
        reservation_id (int): Optional related reservation.
        status (str): Ticket status (e.g., open, in_progress, resolved, closed).
        created_at (datetime): When the ticket was created.
        updated_at (datetime): Last update timestamp.
    """

    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship(back_populates="support_tickets")

    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    order_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    order: Mapped[Optional["Order"]] = relationship(back_populates="support_tickets")

    reservation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reservations.id", ondelete="SET NULL"), nullable=True)
    reservation: Mapped[Optional["Reservation"]] = relationship(back_populates="support_tickets")

    status: Mapped[str] = mapped_column(String(50), default=TicketStatusEnum.OPEN, doc="Ticket status")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
