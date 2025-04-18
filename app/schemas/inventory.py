"""
Inventory schema definitions using Pydantic 2.0.

Defines models for creating, updating, and reading inventory items such as
ingredients, packaging materials, or stock-tracked assets.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class InventoryItemBase(BaseModel):
    """
    Shared fields for inventory item creation and updates.

    Attributes:
        name (str): Name of the inventory item.
        quantity (int): Quantity available in stock.
        unit (str): Unit of measurement (e.g., kg, pieces).
        threshold (int): Threshold to trigger low-stock alerts.
    """
    name: str = Field(..., example="Tomatoes")
    quantity: int = Field(..., example=100)
    unit: str = Field(..., example="kg")
    threshold: Optional[int] = Field(10, example=10, description="Minimum stock level before triggering low-stock alerts")

    model_config = ConfigDict(from_attributes=True)


class InventoryItemCreate(InventoryItemBase):
    """Schema for creating a new inventory item."""
    pass


class InventoryItemUpdate(InventoryItemBase):
    """Schema for updating an existing inventory item."""
    pass


class InventoryItemRead(InventoryItemBase):
    """
    Schema for returning inventory item data to clients.

    Attributes:
        id (int): Unique inventory item ID.
        created_at (datetime): Time the item was added to the system.
        updated_at (datetime): Last time the item was modified.
    """
    id: int
    created_at: datetime
    updated_at: datetime
