"""
Category Service

Handles business logic related to food menu categories.

Includes:
- Creating new categories
- Retrieving individual category details
- Listing all categories
- Updating category information
- Deleting a category

Roles:
- Admin: Create, update, delete
- Public: List and retrieve
"""

from typing import List
from sqlalchemy.orm import Session
from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    """
    Create a new menu category.

    Args:
        db (Session): Database session.
        category_data (CategoryCreate): Input data for the category.

    Returns:
        Category: The newly created category.
    
    Role: Admin
    """
    pass


def get_category(db: Session, category_id: int) -> Category:
    """
    Retrieve a category by its ID.

    Args:
        db (Session): Database session.
        category_id (int): ID of the category.

    Returns:
        Category: The requested category object.
    
    Role: Public
    """
    pass


def list_categories(db: Session) -> List[Category]:
    """
    Retrieve a list of all categories.

    Args:
        db (Session): Database session.

    Returns:
        List[Category]: List of all available categories.
    
    Role: Public
    """
    pass


def update_category(db: Session, category_id: int, update_data: CategoryUpdate) -> Category:
    """
    Update an existing category.

    Args:
        db (Session): Database session.
        category_id (int): ID of the category to update.
        update_data (CategoryUpdate): Fields to update.

    Returns:
        Category: The updated category.
    
    Role: Admin
    """
    pass


def delete_category(db: Session, category_id: int) -> dict:
    """
    Delete a category by its ID.

    Args:
        db (Session): Database session.
        category_id (int): ID of the category to delete.

    Returns:
        dict: Confirmation message.
    
    Role: Admin
    """
    pass
