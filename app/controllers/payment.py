"""
Payment Controller

Handles requests related to payment operations such as initiating, confirming,
and retrieving payment status.

Delegates business logic to the `payment_service` module.

Roles:
- User: Initiate and confirm payments, retrieve status
- Public: Webhook callbacks from payment providers
"""

from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.payment import PaymentInitiate, PaymentConfirm, PaymentStatus
from app.services import payment_service


def initiate_payment_controller(
    payment_data: PaymentInitiate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Initiate a new payment session for an order.
    Role: User
    """
    return payment_service.initiate_payment(db, payment_data, current_user.id)


def get_payment_status_controller(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaymentStatus:
    """
    Retrieve the current status of a specific payment.
    Role: User
    """
    return payment_service.get_payment_status(db, payment_id, current_user.id)


def confirm_payment_controller(
    payment_id: str,
    confirmation_data: PaymentConfirm,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Confirm a payment after front-end processing.
    Role: User
    """
    return payment_service.confirm_payment(db, payment_id, confirmation_data, current_user.id)


async def payment_webhook_controller(
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    """
    Handle payment webhook events from payment providers.
    Role: Public (no auth required)
    """
    return await payment_service.handle_webhook(request, db)
