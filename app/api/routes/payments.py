'''
Payment processing API routes.

Handles payment initiation, verification, status retrieval, and webhook callbacks.
Supports integration with multiple payment gateways (e.g., Stripe, Paymob).
'''

from fastapi import APIRouter, Depends, Request, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.payment import PaymentInitiate, PaymentConfirm, PaymentStatus
from app.controllers import payment as payment_controller

router = APIRouter(prefix="/payments", tags=["payments"])


@cbv(router)
class PaymentAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        summary="Initiate Payment",
        response_description="Initiated payment session info or URL",
    )
    def initiate_payment(
        self,
        payment_data: PaymentInitiate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Initiate a new payment session.

        Accepts order ID, amount, currency, and payment method details,
        then creates and returns a payment token or URL for front-end processing.
        Role: User
        """
        return payment_controller.initiate_payment(self.db, payment_data, current_user.id)

    @router.get(
        "/{payment_id}",
        response_model=PaymentStatus,
        status_code=status.HTTP_200_OK,
        summary="Get Payment Status",
        response_description="Payment status and metadata",
    )
    def get_payment_status(
        self,
        payment_id: str,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve the status of an existing payment.

        Returns details such as 'pending', 'completed', 'failed',
        along with transaction metadata.
        Role: User
        """
        return payment_controller.get_payment_status(self.db, payment_id, current_user.id)

    @router.post(
        "/{payment_id}/confirm",
        status_code=status.HTTP_200_OK,
        summary="Confirm Payment",
        response_description="Confirmation result",
    )
    def confirm_payment(
        self,
        payment_id: str,
        confirmation_data: PaymentConfirm,
        current_user: User = Depends(get_current_user),
    ):
        """
        Confirm a payment after front-end processing.

        Accepts confirmation or callback data and updates payment records
        to reflect success or failure.
        Role: User
        """
        return payment_controller.confirm_payment(self.db, payment_id, confirmation_data, current_user.id)

    @router.post(
        "/webhook",
        status_code=status.HTTP_202_ACCEPTED,
        summary="Payment Webhook Callback",
        response_description="Acknowledges the webhook receipt",
    )
    async def payment_webhook(
        self,
        request: Request,
    ):
        """
        Handle incoming payment gateway webhooks.

        Validates and processes webhook events such as charge succeeded,
        charge failed, or refund events.
        Role: Public
        """
        return await payment_controller.handle_webhook(self.db, request)
