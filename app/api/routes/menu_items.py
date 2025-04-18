"""
Service layer for Menu Item operations.

Encapsulates all business logic related to menu items:
- Creating new menu items
- Listing items with filters
- Retrieving item details
- Updating and deleting items
- Searching by name or description

This service ensures consistency and reusability across the application.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

from app.db.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate


def create_menu_item(db: Session, item_data: MenuItemCreate) -> MenuItem:
    """
    Create a new menu item.

    Args:
        db (Session): SQLAlchemy database session.
        item_data (MenuItemCreate): Data for the new menu item.

    Returns:
        MenuItem: The newly created menu item object.

    Raises:
        HTTPException: If the menu item already exists.
    """
    existing = db.query(MenuItem).filter(MenuItem.name == item_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Menu item already exists")

    item = MenuItem(**item_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_menu_items(
    db: Session,
    category_id: Optional[int] = None,
    vegetarian: Optional[bool] = None
) -> List[MenuItem]:
    """
    List all menu items, with optional filters.

    Args:
        db (Session): SQLAlchemy database session.
        category_id (int, optional): Filter by category.
        vegetarian (bool, optional): Filter by vegetarian flag.

    Returns:
        List[MenuItem]: Filtered list of menu items.
    """
    query = db.query(MenuItem)
    if category_id is not None:
        query = query.filter(MenuItem.category_id == category_id)
    if vegetarian is not None:
        query = query.filter(MenuItem.is_vegetarian == vegetarian)
    return query.all()


def get_menu_item(db: Session, item_id: int) -> MenuItem:
    """
    Retrieve a menu item by ID.

    Args:
        db (Session): SQLAlchemy database session.
        item_id (int): ID of the menu item.

    Returns:
        MenuItem: Retrieved menu item object.

    Raises:
        HTTPException: If the item does not exist.
    """
    item = db.query(MenuItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


def update_menu_item(db: Session, item_id: int, item_data: MenuItemUpdate) -> MenuItem:
    """
    Update an existing menu item.

    Args:
        db (Session): SQLAlchemy database session.
        item_id (int): ID of the item to update.
        item_data (MenuItemUpdate): Fields to update.

    Returns:
        MenuItem: Updated item object.
    """
    item = get_menu_item(db, item_id)
    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, item_id: int) -> dict:
    """
    Delete a menu item by ID.

    Args:
        db (Session): SQLAlchemy database session.
        item_id (int): ID of the item to delete.

    Returns:
        dict: Success message.
    """
    item = get_menu_item(db, item_id)
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted"}


def search_menu_items(db: Session, query: str) -> List[MenuItem]:
    """
    Search for menu items by name or description.

    Args:
        db (Session): SQLAlchemy database session.
        query (str): Search term.

    Returns:
        List[MenuItem]: List of matching items.
    """
    return db.query(MenuItem).filter(
        (MenuItem.name.ilike(f"%{query}%")) |
        (MenuItem.description.ilike(f"%{query}%"))
    ).all()
