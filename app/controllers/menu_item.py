"""
Menu Item Controller

Handles incoming requests related to restaurant menu items and delegates
the business logic to the menu_service module.

Supports operations such as:
- Create, retrieve, update, delete menu items
- Filter by category or vegetarian
- Search by name or description

Role access: Admin (except public search).
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.db.models.user import User
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemRead
from app.services import menu_service


def create_menu_item(
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> MenuItemRead:
    """
    Create a new menu item (Admin only).
    """
    return menu_service.create_menu_item(db, item_data)


def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> MenuItemRead:
    """
    Retrieve a specific menu item by its ID (Admin only).
    """
    return menu_service.get_menu_item(db, item_id)


def list_menu_items(
    category_id: Optional[int] = None,
    vegetarian: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> List[MenuItemRead]:
    """
    List all menu items, optionally filtered by category or vegetarian flag (Admin only).
    """
    return menu_service.list_menu_items(db, category_id, vegetarian)


def update_menu_item(
    item_id: int,
    item_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> MenuItemRead:
    """
    Update an existing menu item (Admin only).
    """
    return menu_service.update_menu_item(db, item_id, item_data)


def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> dict:
    """
    Delete a menu item by ID (Admin only).
    """
    return menu_service.delete_menu_item(db, item_id)


def search_menu_items(
    query: str,
    db: Session = Depends(get_db)
) -> List[MenuItemRead]:
    """
    Public search for menu items by name or description.
    """
    return menu_service.search_menu_items(db, query)
