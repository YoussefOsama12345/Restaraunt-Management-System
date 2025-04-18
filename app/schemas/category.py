"""
Category schema definitions using Pydantic 2.0.

Defines request and response models for food menu categories.
Supports creation, updating, and returning category information.
"""

from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    """
    Base schema shared across creation and update models.

    Attributes:
        name (str): Name of the category (e.g., "Starters", "Drinks").
        description (str): Optional description for the category.
    """
    name: str = Field(..., example="Desserts", max_length=100)
    description: str = Field(..., example="Sweet items served after main course.")

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass


class CategoryUpdate(CategoryBase):
    """Schema for updating an existing category."""
    pass


class CategoryRead(CategoryBase):
    """
    Schema for returning category data to the client.

    Attributes:
        id (int): Unique ID of the category.
    """
    id: int
