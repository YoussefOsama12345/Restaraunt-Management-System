# app/db/models/review.py

"""
Review database model.

Stores user-submitted reviews for either menu items or restaurants.
Includes rating (1–5), optional comment, and relational references.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.user import User
from app.db.models.menu_item import MenuItem
from app.db.models.restaurant import Restaurant


class Review(Base):
    """
    Represents a review given by a user for a menu item or a restaurant.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user who wrote the review.
        menu_item_id (int): Foreign key to the reviewed menu item (nullable).
        restaurant_id (int): Foreign key to the reviewed restaurant (nullable).
        rating (float): Rating score (1.0 to 5.0).
        comment (str): Optional user comment.
        created_at (datetime): Timestamp of review creation.
    """

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship(back_populates="reviews")

    menu_item_id: Mapped[Optional[int]] = mapped_column(ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=True)
    menu_item: Mapped[Optional[MenuItem]] = relationship(back_populates="reviews")

    restaurant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=True)
    restaurant: Mapped[Optional[Restaurant]] = relationship(back_populates="reviews")

    rating: Mapped[float] = mapped_column(nullable=False, doc="Rating between 1 and 5")
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
