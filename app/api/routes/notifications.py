""
"""Notification API Routes

This module defines API endpoints for sending notifications to users and admins:
- Reservation reminders
- Order confirmations
- Order receipts
- Admin broadcast alerts

All endpoints require authentication.
"""

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.controllers import notification as notification_controller

router = APIRouter(prefix="/notifications", tags=["notifications"])


@cbv(router)
class NotificationAPI:
    db: Session = Depends(get_db)

    @router.post("/reservation-reminder/{reservation_id}", status_code=status.HTTP_202_ACCEPTED)
    def reservation_reminder(self, reservation_id: int, current_user=Depends(get_current_user)):
        """
        Send a reminder email for a reservation.

        Args:
            reservation_id: ID of the reservation to remind.
            current_user: Authenticated user (typically customer).

        Returns:
            Success message confirming the email was sent.
        Role: User
        """
        return notification_controller.reservation_reminder(self.db, reservation_id, current_user)

    @router.post("/order-confirmation/{order_id}", status_code=status.HTTP_202_ACCEPTED)
    def order_confirmation(self, order_id: int, current_user=Depends(get_current_user)):
        """
        Send an email confirmation after order placement.

        Args:
            order_id: ID of the order.
            current_user: Authenticated user (order owner).

        Returns:
            Success message confirming the email was sent.
        Role: User
        """
        return notification_controller.order_confirmation(self.db, order_id, current_user)

    @router.post("/order-receipt/{order_id}", status_code=status.HTTP_202_ACCEPTED)
    def order_receipt(self, order_id: int, current_user=Depends(get_current_user)):
        """
        Send a receipt email for an order.

        Args:
            order_id: ID of the order.
            current_user: Authenticated user requesting the receipt.

        Returns:
            Success message confirming the email was sent.
        Role: User
        """
        return notification_controller.order_receipt(self.db, order_id, current_user)

    @router.post("/admin-alert", status_code=status.HTTP_202_ACCEPTED)
    def notify_admins(self, message: str, subject: str = "Admin Notification", current_user=Depends(get_current_admin)):
        """
        Send a custom alert to all admin users.

        Args:
            message: Notification message body.
            subject: Optional subject line.
            current_user: Authenticated user initiating the alert.

        Returns:
            Success message confirming the email was sent.
        Role: Admin
        """
        return notification_controller.notify_admins(self.db, message, subject, current_user)
""
