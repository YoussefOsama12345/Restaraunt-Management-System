"""
Inventory Controller

Handles inventory operations for ingredients and stock management.
Delegates core business logic to the inventory_service module.
Only accessible by admin users.
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.deps import get_current_admin
from app.db.models.user import User
from app.schemas.inventory import InventoryItemCreate, InventoryItemUpdate
from app.schemas.inventory import InventoryItemRead
from app.services import inventory_service


def create_inventory_item(
    item_data: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> InventoryItemRead:
    """
    Add a new inventory item (e.g., ingredient or supply).

    Role: Admin
    """
    return inventory_service.create_inventory(db, item_data)


def list_inventory_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> List[InventoryItemRead]:
    """
    Retrieve a list of all inventory items.

    Role: Admin
    """
    return inventory_service.get_all_inventory(db)


def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> InventoryItemRead:
    """
    Retrieve a specific inventory item by ID.

    Role: Admin
    """
    return inventory_service.get_inventory_by_id(db, item_id)


def update_inventory_item(
    item_id: int,
    item_data: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> InventoryItemRead:
    """
    Update details (e.g., quantity, threshold) of an inventory item.

    Role: Admin
    """
    return inventory_service.update_inventory(db, item_id, item_data)


def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> dict:
    """
    Remove an inventory item from the system.

    Role: Admin
    """
    return inventory_service.delete_inventory(db, item_id)


def list_low_stock_items(
    threshold: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> List[InventoryItemRead]:
    """
    List inventory items below the defined stock threshold.

    Role: Admin
    """
    return inventory_service.get_low_stock_items(db, threshold)
