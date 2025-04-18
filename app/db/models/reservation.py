# app/db/models/reservation.py

"""
Reservation database model.

Represents a table reservation made by a user, including time, date,
guest count, and optional special requests.
"""

from datetime import datetime, time, date
from typing import Optional

from sqlalchemy import ForeignKey, String,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.user import User

class Reservation(Base):
    """
    Represents a reservation made by a user for dining.

    Attributes:
        id (int): Unique reservation identifier.
        user_id (int): Foreign key to the user who made the reservation.
        reservation_date (date): The date for the reservation.
        reservation_time (time): The time of the reservation.
        guest_count (int): Number of guests for the reservation.
        status (str): Reservation status (e.g., 'pending', 'confirmed', 'cancelled').
        special_requests (str): Optional notes like allergies or seating preferences.
        confirmed (bool): Whether the reservation is confirmed.
        created_at (datetime): Timestamp when reservation was created.
        updated_at (datetime): Timestamp when reservation was last updated.
    """

    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    reservation_date: Mapped[date] = mapped_column(nullable=False, doc="Date of the reservation")
    reservation_time: Mapped[time] = mapped_column(nullable=False, doc="Time of the reservation")
    guest_count: Mapped[int] = mapped_column(nullable=False, doc="Number of guests")
    status: Mapped[str] = mapped_column(String(20), default="pending", doc="Reservation status")
    special_requests: Mapped[Optional[str]] = mapped_column(Text, nullable=True, doc="Optional requests")

    confirmed: Mapped[bool] = mapped_column(default=False, doc="Whether reservation is confirmed")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship("user", back_populates="reservations")
