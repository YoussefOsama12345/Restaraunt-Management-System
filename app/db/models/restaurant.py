# app/db/models/restaurant.py

"""
Restaurant database model.

Represents a restaurant entity with details such as name, location, cuisine type,
and contact information. Used to associate menu items, reservations, and reviews.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Restaurant(Base):
    """
    Represents a restaurant entity in the system.

    Attributes:
        id (int): Unique identifier for the restaurant.
        name (str): Name of the restaurant.
        description (str): Optional description or bio.
        location (str): Physical location or address.
        cuisine_type (str): Type of cuisine offered (e.g., Italian, Indian).
        phone (str): Contact number.
        is_active (bool): Indicates if the restaurant is currently active.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """

    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    cuisine_type: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
