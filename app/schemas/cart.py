"""
Cart schema definitions using Pydantic 2.0.

Defines models for creating, updating, and retrieving cart items for authenticated users.
Each cart item represents a menu item selected by the user and its desired quantity.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CartItemBase(BaseModel):
    """
    Shared base schema for cart item fields.

    Attributes:
        menu_item_id (int): ID of the selected menu item.
        quantity (int): Quantity of the item added to the cart.
    """
    menu_item_id: int = Field(..., description="ID of the selected menu item")
    quantity: int = Field(..., gt=0, description="Quantity of the item in the cart")

    model_config = ConfigDict(from_attributes=True)


class CartItemCreate(CartItemBase):
    """Schema for adding a new item to the user's cart."""
    pass


class CartItemUpdate(BaseModel):
    """
    Schema for updating the quantity of an item in the cart.

    Attributes:
        quantity (int): Updated quantity value.
    """
    quantity: int = Field(..., gt=0, description="New quantity for the cart item")


class CartItemRead(CartItemBase):
    """
    Schema for reading cart item details from the system.

    Attributes:
        id (int): Unique identifier of the cart item.
        user_id (int): ID of the user who owns the cart.
    """
    id: int
    user_id: int
