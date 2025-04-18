"""
MenuItem schema definitions using Pydantic 2.0.

Defines models for menu item creation, update, and response including
name, price, category, image, availability, and dietary flags.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class MenuItemBase(BaseModel):
    """
    Shared fields for menu item creation and updates.

    Attributes:
        name (str): Name of the menu item.
        description (str): Description of the dish or item.
        price (float): Price in local currency.
        image_url (str): URL pointing to the item's image.
        available (bool): Whether the item is available.
        is_vegetarian (bool): Whether the item is vegetarian.
        category_id (int): ID of the category the item belongs to.
    """
    name: str = Field(..., example="Margherita Pizza")
    description: Optional[str] = Field(None, example="Classic pizza with tomato, mozzarella, and basil.")
    price: float = Field(..., example=9.99)
    image_url: Optional[str] = Field(None, example="https://example.com/images/pizza.jpg")
    available: Optional[bool] = Field(default=True)
    is_vegetarian: Optional[bool] = Field(default=False)
    category_id: Optional[int] = Field(None, description="ID of the category this item belongs to")

    model_config = ConfigDict(from_attributes=True)


class MenuItemCreate(MenuItemBase):
    """Schema for creating a new menu item."""
    pass


class MenuItemUpdate(MenuItemBase):
    """Schema for updating an existing menu item."""
    pass


class MenuItemRead(MenuItemBase):
    """
    Schema for returning a menu item to clients.

    Attributes:
        id (int): Unique identifier of the menu item.
    """
    id: int
