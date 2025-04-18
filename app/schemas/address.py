"""
Address schema definitions using Pydantic 2.0.

These models define the structure for creating, updating, and reading user address data,
including validation rules and example values for OpenAPI documentation.

Used for user address book management in delivery and billing flows.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AddressBase(BaseModel):
    """
    Shared base schema for address fields.

    Attributes:
        street (str): Street name and number (e.g., "123 Elm St").
        city (str): City name (e.g., "New York").
        state (Optional[str]): State or province (e.g., "NY").
        country (str): Country name (e.g., "USA").
        zip_code (str): Postal or ZIP code (e.g., "10001").
        is_default (Optional[bool]): Whether this is the user's default address.
        label (Optional[str]): Optional label for address like "Home" or "Work".
    """
    street: str = Field(..., example="123 Elm St")
    city: str = Field(..., example="New York")
    state: Optional[str] = Field(None, example="NY")
    country: str = Field(..., example="USA")
    zip_code: str = Field(..., example="10001")
    is_default: Optional[bool] = Field(False, description="Whether this is the user's default address")
    label: Optional[str] = Field(None, example="Home or Work")

    model_config = ConfigDict(from_attributes=True)

class AddressCreate(AddressBase):
    """Schema for creating a new address record."""
    pass

class AddressUpdate(AddressBase):
    """Schema for updating an existing address record."""
    pass

class AddressRead(AddressBase):
    """
    Schema for returning address data to the client.

    Attributes:
        id (int): Unique identifier of the address.
        user_id (int): ID of the user who owns this address.
    """
    id: int
    user_id: int
