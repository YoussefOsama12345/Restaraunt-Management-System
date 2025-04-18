"""
Schemas for managing user accounts in the application.

This module defines the data models used for creating, updating, and retrieving user profiles.
It includes the following schemas:
- UserBase: Base schema for common user attributes.
- UserCreate: Schema for creating a new user.
- UserUpdate: Schema for updating an existing user.
- UserRead: Schema for returning user data to the client.

Each schema uses Pydantic for data validation and serialization.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserBase(BaseModel):
    """
    Base schema for user-related data.

    Attributes:
        username (str): The unique username of the user.
        email (EmailStr): The email address of the user.
        full_name (Optional[str]): The full name of the user.
        phone_number (Optional[str]): The contact number of the user.
        is_active (Optional[bool]): Indicates whether the user's account is active (default is True).
        is_admin (Optional[bool]): Indicates whether the user has admin privileges (default is False).
    """
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")
    phone_number: Optional[str] = Field(None, example="+1234567890")
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Inherits from UserBase and is used to validate data when creating a new user.
    This schema ensures that all required fields are provided for user creation.
    """
    password: str = Field(..., min_length=8, example="securepassword123")

class UserUpdate(UserBase):
    """
    Schema for updating an existing user.

    Inherits from UserBase and is used to validate data when updating a user's information.
    This schema allows modification of fields such as full_name, phone_number, and is_active status.
    """
    pass

class UserRead(UserBase):
    """
    Schema for returning user data to the client.

    Inherits from UserBase and includes additional fields for user identification.

    Attributes:
        id (int): The unique identifier for the user.
    """
    id: int
