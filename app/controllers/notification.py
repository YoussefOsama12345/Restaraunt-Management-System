"""
Notification Controller

Handles actions related to sending user and admin notifications, including:
- Reservation reminders
- Order confirmations and receipts
- Admin broadcast alerts

Delegates business logic to the `notification_service` module.

Roles:
- User: Reservation/order notifications
- Admin: Broadcast alerts to other admins
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_admin
from app.db.database import get_db
from app.db.models.user import User
from app.services import notification_service


def send_reservation_reminder_controller(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Sends a reminder email to the user for a specific reservation.
    Role: User
    """
    return notification_service.send_reservation_reminder(db, reservation_id, current_user.id)


def send_order_confirmation_controller(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Sends an order confirmation email to the user.
    Role: User
    """
    return notification_service.send_order_confirmation(db, order_id, current_user.id)


def send_order_receipt_controller(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Sends an order receipt email to the user.
    Role: User
    """
    return notification_service.send_order_receipt(db, order_id, current_user.id)


def send_admin_alert_controller(
    message: str,
    subject: str = "Admin Notification",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> dict:
    """
    Sends a broadcast alert to all admin users.
    Role: Admin
    """
    return notification_service.send_admin_notification(db, message, subject)
