from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class RestaurantBase(BaseModel):
    """
    Base schema for restaurant-related data.

    Attributes:
        name (str): The name of the restaurant.
        address (str): The physical address of the restaurant.
        contact (Optional[str]): The contact number for the restaurant, if available.
        hours (Optional[str]): The operating hours of the restaurant (e.g., "9am - 11pm").
        is_active (Optional[bool]): Indicates whether the restaurant is currently active (default is True).
    """
    name: str
    address: str
    contact: Optional[str] = None
    hours: Optional[str] = Field(None, example="9am - 11pm")
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)

class RestaurantCreate(RestaurantBase):
    """
    Schema for creating a new restaurant.

    Inherits from RestaurantBase and is used to validate data when creating a new restaurant.
    """
    pass

class RestaurantUpdate(RestaurantBase):
    """
    Schema for updating an existing restaurant.

    Inherits from RestaurantBase and is used to validate data when updating a restaurant's information.
    """
    pass

class RestaurantRead(RestaurantBase):
    """
    Schema for returning restaurant data to the client.

    Inherits from RestaurantBase and includes additional fields for restaurant identification.

    Attributes:
        id (int): The unique identifier for the restaurant.
    """
    id: int