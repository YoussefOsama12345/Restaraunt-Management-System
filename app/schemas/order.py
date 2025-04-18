"""
Schemas for order, payment, reservation, and restaurant models.
Includes request/response definitions for API input/output validation.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class OrderItem(BaseModel):
    """
    Represents an item in an order.

    Attributes:
        menu_item_id (int): The ID of the menu item being ordered.
        quantity (int): The quantity of the menu item being ordered.
    """
    menu_item_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    """
    Base schema for order-related data.

    Attributes:
        status (Optional[str]): The current status of the order (default is "pending").
        total_amount (float): The total amount for the order.
        payment_method (str): The method of payment used for the order.
        delivery_address_id (Optional[int]): The ID of the delivery address associated with the order.
    """
    status: Optional[str] = Field("pending", example="confirmed")
    total_amount: float = Field(..., example=42.99)
    payment_method: str = Field(..., example="credit_card")
    delivery_address_id: Optional[int] = Field(None)

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    """
    Schema for creating a new order.

    Inherits from OrderBase and adds the items being ordered.

    Attributes:
        items (List[OrderItem]): A list of items included in the order.
    """
    items: List[OrderItem]

class OrderUpdateStatus(BaseModel):
    """
    Schema for updating the status of an existing order.

    Attributes:
        status (str): The new status of the order (e.g., "out_for_delivery").
    """
    status: str = Field(..., example="out_for_delivery")

class OrderRead(OrderBase):
    """
    Schema for returning order data to the client.

    Inherits from OrderBase and includes additional fields for order identification.

    Attributes:
        id (int): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        created_at (datetime): The timestamp when the order was created.
        items (List[OrderItem]): A list of items included in the order.
    """
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItem]