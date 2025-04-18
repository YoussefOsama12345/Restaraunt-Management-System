"""
Address database model.

Stores delivery and billing address details for authenticated users.
Each address can be marked as default and includes city, street, postal code, and more.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.db.database import Base
from app.db.models.user import User  # Ensure this import exists for relationship typing


class Address(Base):
    """
    Represents a user's address record.

    Attributes:
        id (int): Unique identifier for the address.
        user_id (int): Foreign key referencing the user who owns this address.
        street (str): The street and number of the address.
        city (str): The city where the address is located.
        state (Optional[str]): The state or province.
        country (str): The country of the address.
        zip_code (str): Postal/ZIP code of the address.
        is_default (bool): Indicates if this is the user's default address.
        label (Optional[str]): Optional label like "Home", "Work", etc.
    """

    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False, doc="Street and number", length=255)
    city: Mapped[str] = mapped_column(nullable=False, doc="City", length=100)
    state: Mapped[Optional[str]] = mapped_column(nullable=True, doc="State or province", length=100)
    country: Mapped[str] = mapped_column(nullable=False, doc="Country", length=100)
    zip_code: Mapped[str] = mapped_column(nullable=False, doc="Postal/ZIP code", length=20)
    is_default: Mapped[bool] = mapped_column(default=False, doc="Whether this address is the default one")
    label: Mapped[Optional[str]] = mapped_column(nullable=True, doc="Optional label such as 'Home' or 'Work'", length=50)
    user: Mapped["User"] = relationship(back_populates="addresses")
