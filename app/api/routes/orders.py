"""
Order management API routes.

Handles placing new orders, retrieving order details, listing orders,
updating order status, cancellation, and tracking delivery information.
All endpoints require user authentication.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdateStatus
from app.controllers import order as order_controller

router = APIRouter(prefix="/orders", tags=["orders"])


@cbv(router)
class OrderAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=dict,
        status_code=status.HTTP_201_CREATED,
        summary="Create Order",
    )
    def create_order(
        self,
        order_data: OrderCreate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Create a new order for the authenticated user.

        Args:
            order_data (OrderCreate): Information about the order including cart, address, and payment.
            current_user (User): The currently logged-in user.

        Returns:
            dict: Success message or order confirmation details.
        """
        return order_controller.create_order(self.db, order_data, current_user.id)

    @router.get(
        "/{order_id}",
        response_model=OrderRead,
        status_code=status.HTTP_200_OK,
        summary="Get Order",
    )
    def get_order(
        self,
        order_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve a specific order by its ID.

        Args:
            order_id (int): The ID of the order to retrieve.
            current_user (User): The currently logged-in user.

        Returns:
            OrderRead: Full order information including items and status.
        """
        return order_controller.get_order(self.db, order_id, current_user.id)

    @router.get(
        "/",
        response_model=List[OrderRead],
        status_code=status.HTTP_200_OK,
        summary="List User Orders",
    )
    def list_orders(
        self,
        current_user: User = Depends(get_current_user),
    ):
        """
        List all orders placed by the current user.

        Args:
            current_user (User): The currently logged-in user.

        Returns:
            List[OrderRead]: List of order records.
        """
        return order_controller.list_orders(self.db, current_user.id)

    @router.patch(
        "/{order_id}/status",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Update Order Status",
    )
    def update_order_status(
        self,
        order_id: int,
        status_data: OrderUpdateStatus,
        current_user: User = Depends(get_current_user),
    ):
        """
        Update the status of an existing order (e.g., to 'delivered').

        Args:
            order_id (int): ID of the order to update.
            status_data (OrderUpdateStatus): New status value.
            current_user (User): The currently logged-in user.

        Returns:
            dict: Confirmation of status update.
        """
        return order_controller.update_order_status(self.db, order_id, status_data, current_user.id)

    @router.post(
        "/{order_id}/cancel",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Cancel Order",
    )
    def cancel_order(
        self,
        order_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Cancel a specific order if it's still eligible for cancellation.

        Args:
            order_id (int): ID of the order to cancel.
            current_user (User): The currently logged-in user.

        Returns:
            dict: Confirmation of cancellation.
        """
        return order_controller.cancel_order(self.db, order_id, current_user.id)

    @router.get(
        "/{order_id}/track",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Track Order",
    )
    def track_order(
        self,
        order_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Track the delivery status of an order.

        Args:
            order_id (int): ID of the order to track.
            current_user (User): The currently logged-in user.

        Returns:
            dict: Tracking information such as delivery status and ETA.
        """
        return order_controller.track_order(self.db, order_id, current_user.id)
