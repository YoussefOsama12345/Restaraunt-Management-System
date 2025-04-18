"""
Inventory management API routes.

This module defines FastAPI routes for managing inventory items such as ingredients,
supplies, and packaging materials used in the restaurant system. It supports:
- Creating inventory items
- Retrieving individual or all inventory records
- Updating existing items
- Deleting inventory records
- Listing low-stock alerts

Access Control:
All endpoints are restricted to users with admin privileges.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.database import get_db
from app.db.models.inventory import InventoryItem
from app.db.models.user import User
from app.schemas.inventory import InventoryItemCreate, InventoryItemUpdate
from app.controllers import inventory

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(get_current_admin)],
)

logger = logging.getLogger("inventory")
logger.setLevel(logging.INFO)

@cbv(router)
class InventoryAPI:
    """
    InventoryAPI class-based view for all inventory-related endpoints.

    Uses controller logic defined in app.controllers.inventory.
    All operations are accessible only by admin users.
    """
    
    db: Session = Depends(get_db)

    def create_inventory_item(
        self,
        item_data: InventoryItemCreate,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Create a new inventory item.

        Args:
            item_data (InventoryItemCreate): Information about the item to add.
            current_user (User): Authenticated admin user.

        Returns:
            InventoryItem: Newly created inventory item object.
        """
        return inventory.create_inventory_item(self.db, item_data)

    def list_inventory_items(
        self,
        current_user: User = Depends(get_current_admin),
    ):
        """
        List all inventory items.

        Args:
            current_user (User): Authenticated admin user.

        Returns:
            List[InventoryItem]: All inventory records in the database.
        """
        return inventory.list_inventory_items(self.db)

    def get_inventory_item(
        self,
        item_id: int,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Retrieve a specific inventory item by ID.

        Args:
            item_id (int): ID of the inventory item.
            current_user (User): Authenticated admin user.

        Returns:
            InventoryItem: Inventory item record.
        """
        return inventory.get_inventory_item(self.db, item_id)

    def update_inventory_item(
        self,
        item_id: int,
        item_data: InventoryItemUpdate,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Update an existing inventory item.

        Args:
            item_id (int): ID of the inventory item to update.
            item_data (InventoryItemUpdate): Updated inventory data.
            current_user (User): Authenticated admin user.

        Returns:
            InventoryItem: Updated inventory item.
        """
        return inventory.update_inventory_item(self.db, item_id, item_data)

    def delete_inventory_item(
        self,
        item_id: int,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Delete an inventory item by ID.

        Args:
            item_id (int): ID of the inventory item to delete.
            current_user (User): Authenticated admin user.

        Returns:
            dict: Confirmation message.
        """
        return inventory.delete_inventory_item(self.db, item_id)

    def list_low_stock_items(
        self,
        threshold: int = 0,
        current_user: User = Depends(get_current_admin),
    ):
        """
        List inventory items with quantity below the threshold.

        Args:
            threshold (int): Stock quantity threshold. Default is 0.
            current_user (User): Authenticated admin user.

        Returns:
            List[InventoryItem]: Inventory items with stock below threshold.
        """
        return inventory.list_low_stock_items(self.db, threshold)
