"""
Delivery Task Service

Handles logic for assigning and managing delivery tasks:

- Assigning orders to delivery drivers
- Retrieving assigned deliveries
- Updating delivery status (en route, delivered, failed)
- Confirming delivery with OTP or proof

Roles:
- Admin (assign deliveries)
- Driver (view, update, confirm)
"""

from typing import List
from sqlalchemy.orm import Session
from app.db.models.delivery_task import DeliveryTask
from app.schemas.delivery_task import DeliveryAssign, DeliveryStatusUpdate, DeliveryConfirmOTP


def assign_delivery(db: Session, order_id: int, driver_id: int) -> DeliveryTask:
    """
    Assign an order to a delivery driver.

    Args:
        db (Session): Database session.
        order_id (int): ID of the order to assign.
        driver_id (int): ID of the driver to assign to.

    Returns:
        DeliveryTask: The newly created delivery task.

    Role: Admin
    """
    pass


def get_assigned_deliveries(db: Session, driver_id: int) -> List[DeliveryTask]:
    """
    Retrieve all deliveries assigned to a specific driver.

    Args:
        db (Session): Database session.
        driver_id (int): ID of the delivery driver.

    Returns:
        List[DeliveryTask]: List of delivery tasks.

    Role: Driver
    """
    pass


def update_delivery_status(db: Session, task_id: int, new_status: str, driver_id: int) -> DeliveryTask:
    """
    Update the delivery status (e.g., en_route, delivered, failed).

    Args:
        db (Session): Database session.
        task_id (int): ID of the delivery task.
        new_status (str): New status value.
        driver_id (int): ID of the driver making the update.

    Returns:
        DeliveryTask: Updated delivery task.

    Role: Driver
    """
    pass


def confirm_delivery_with_otp(db: Session, task_id: int, otp: str, driver_id: int) -> dict:
    """
    Confirm the delivery completion using OTP verification.

    Args:
        db (Session): Database session.
        task_id (int): ID of the delivery task.
        otp (str): One-time password for delivery confirmation.
        driver_id (int): ID of the confirming driver.

    Returns:
        dict: Success or failure confirmation.

    Role: Driver
    """
    pass
