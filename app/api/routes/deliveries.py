"""
Delivery management API routes for drivers.

Provides endpoints for drivers to retrieve assigned deliveries,
assign orders to delivery personnel, update delivery status,
and confirm completion with OTP or proof.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user, get_current_admin, get_current_delivery
from app.db.models.user import User
from app.controllers import delivery_task as delivery_controller  

router = APIRouter(
    prefix="/deliveries",
    tags=["deliveries"]
)

@cbv(router)
class DeliveryAPI:
    db: Session = Depends(get_db)

    @router.get(
        "/assigned/{driver_id}",
        status_code=status.HTTP_200_OK,
        summary="Get Assigned Deliveries",
        response_description="List of deliveries assigned to the driver",
        dependencies=[Depends(get_current_delivery)]
    )
    def get_assigned_deliveries(self, driver_id: int, current_user: User = Depends(get_current_user)):
        """
        Retrieve all delivery tasks assigned to a specific driver.

        Returns a list of pending or in-progress deliveries for the given driver ID.
        Role: Driver
        """
        return delivery_controller.get_assigned_deliveries(self.db, driver_id)

    @router.post(
        "/assign",
        status_code=status.HTTP_201_CREATED,
        summary="Assign Delivery Task",
        response_description="Delivery task successfully assigned",
        dependencies=[Depends(get_current_admin)]
    )
    def assign_delivery(self, order_id: int, driver_id: int, current_user: User = Depends(get_current_admin)):
        """
        Assign an order to a delivery driver.

        Creates a new delivery task with status 'assigned' linking the order and driver.
        Role: Admin
        """
        return delivery_controller.assign_delivery(self.db, order_id, driver_id)

    @router.post(
        "/{task_id}/status",
        status_code=status.HTTP_200_OK,
        summary="Update Delivery Status",
        response_description="Updated status of delivery task",
        dependencies=[Depends(get_current_delivery)]
    )
    def update_delivery_status(
        self, task_id: int, status: str, current_user: User = Depends(get_current_delivery)
    ):
        """
        Update the status of an existing delivery task.

        Allows drivers to mark tasks as 'en_route', 'delivered', or 'failed'.
        Role: Driver
        """
        return delivery_controller.update_delivery_status(self.db, task_id, status)

    @router.post(
        "/{task_id}/confirm",
        status_code=status.HTTP_200_OK,
        summary="Confirm Delivery via OTP",
        response_description="Marks delivery as complete after OTP confirmation",
        dependencies=[Depends(get_current_delivery)]
    )
    def confirm_delivery(self, task_id: int, otp: str, current_user: User = Depends(get_current_delivery)):
        """
        Confirm delivery completion with OTP verification.

        Validates the provided OTP and marks the delivery task as 'delivered' when successful.
        Role: Driver
        """
        return delivery_controller.confirm_delivery(self.db, task_id, otp)
