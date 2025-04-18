# app/db/models/menu_item.py

"""
MenuItem database model.

Represents a food or beverage item available on the restaurant's menu.
Includes pricing, description, availability, category, and dietary flags.
"""

from sqlalchemy import String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base  
from typing import Optional
from app.db.models.category import Category  



class MenuItem(Base):
    """
    Represents a menu item available for order.

    Attributes:
        id (int): Unique identifier for the menu item.
        name (str): Name of the dish or beverage.
        description (str): Description of the item.
        price (float): Selling price.
        image_url (str): URL of the item's image.
        available (bool): Whether the item is currently available.
        is_vegetarian (bool): Whether the item is suitable for vegetarians.
        category_id (int): Foreign key to the category this item belongs to.
    """

    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, doc="Name of the menu item")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, doc="Detailed description of the item")
    price: Mapped[float] = mapped_column(nullable=False, doc="Price of the menu item")
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, doc="Image URL of the menu item")
    available: Mapped[bool] = mapped_column(default=True, doc="Whether the item is available")
    is_vegetarian: Mapped[bool] = mapped_column(default=False, doc="Is the item vegetarian")

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category: Mapped[Category] = relationship("category",back_populates="menu_items")
