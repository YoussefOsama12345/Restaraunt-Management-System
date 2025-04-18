"""
Order Controller

Handles user requests related to placing and managing food orders.

Delegates business logic to the `order_service` module and enforces
authentication and user-specific access control.

Roles:
- User: Place, view, update, cancel, and track orders
"""

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdateStatus
from app.services import order_service


def create_order_controller(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Create a new food order.
    Role: User
    """
    return order_service.create_order(db, order_data, current_user.id)


def get_order_controller(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderRead:
    """
    Get details of a specific order.
    Role: User
    """
    return order_service.get_order(db, order_id, current_user.id)


def list_orders_controller(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[OrderRead]:
    """
    List all orders of the current user.
    Role: User
    """
    return order_service.list_user_orders(db, current_user.id)


def update_order_status_controller(
    order_id: int,
    status_data: OrderUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Update the status of a specific order.
    Role: User
    """
    return order_service.update_order_status(db, order_id, status_data.status, current_user.id)


def cancel_order_controller(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Cancel a specific order.
    Role: User
    """
    return order_service.cancel_order(db, order_id, current_user.id)


def track_order_controller(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Track the current status and delivery progress of an order.
    Role: User
    """
    return order_service.track_order(db, order_id, current_user.id)
