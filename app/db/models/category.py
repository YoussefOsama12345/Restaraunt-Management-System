# app/db/models/category.py

"""
Category database model.

Defines menu item categories such as starters, mains, desserts, and beverages.
Each category can have multiple menu items associated with it.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class Category(Base):
    """
    Represents a food category for menu organization.

    Attributes:
        id (int): Primary key.
        name (str): Name of the category (e.g., "Starters", "Main Course").
        description (str): Optional description of the category.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, doc="Category name")
    description: Mapped[str] = mapped_column(String(255), nullable=True, doc="Optional category description")

    menu_items = relationship("MenuItem", back_populates="category", cascade="all, delete-orphan")
