# app/db/models/inventory_item.py

"""
InventoryItem database model.

Represents ingredients or stock items used in the restaurant system.
Tracks quantity, units, and low-stock thresholds for inventory monitoring.
"""

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class InventoryItem(Base):
    """
    Represents an inventory item used for managing restaurant stock.

    Attributes:
        id (int): Unique item ID.
        name (str): Name of the inventory item (e.g., Tomato, Box, Napkin).
        quantity (float): Current quantity available.
        unit (str): Unit of measurement (e.g., kg, liters, pieces).
        threshold (float): Minimum quantity before the item is considered low-stock.
    """

    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, doc="Name of the item")
    quantity: Mapped[float] = mapped_column(nullable=False, default=0.0, doc="Current stock quantity")
    unit: Mapped[str] = mapped_column(String(20), nullable=False, doc="Measurement unit (kg, L, pcs, etc.)")
    threshold: Mapped[float] = mapped_column(nullable=False, default=0.0, doc="Threshold for low-stock alerts")
