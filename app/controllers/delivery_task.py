"""
Delivery Task Controller

Manages delivery task operations for drivers and admins.
Handles assigning deliveries, updating delivery status, and confirming delivery completion.
Delegates core logic to the delivery_service module.
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.deps import get_current_user, get_current_admin, get_current_delivery
from app.db.models.user import User
from app.services import delivary_task as delivery_service
from app.schemas.delivery_task import DeliveryRead


def get_assigned_deliveries(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_delivery)
) -> List[DeliveryRead]:
    """
    Retrieve deliveries assigned to a specific driver.

    Role: Driver
    """
    return delivery_service.get_driver_deliveries(db, driver_id)


def assign_delivery_task(
    order_id: int,
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> DeliveryRead:
    """
    Assign an order to a delivery driver.

    Role: Admin
    """
    return delivery_service.assign_delivery(db, order_id, driver_id)


def update_delivery_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_delivery)
) -> dict:
    """
    Update the status of a delivery task.

    Role: Driver
    """
    return delivery_service.update_delivery_status(db, task_id, status)


def confirm_delivery_otp(
    task_id: int,
    otp: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_delivery)
) -> dict:
    """
    Confirm delivery completion using OTP.

    Role: Driver
    """
    return delivery_service.confirm_delivery(db, task_id, otp)
