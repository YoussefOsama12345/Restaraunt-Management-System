from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PaymentInitiate(BaseModel):
    """
    Schema for initiating a payment.

    Attributes:
        order_id (int): The ID of the order for which the payment is being made.
        amount (float): The total amount to be charged for the order.
        currency (str): The currency in which the payment is made (default is "USD").
        method (str): The payment method used (e.g., "stripe", "paypal").
    """
    order_id: int
    amount: float
    currency: str = Field("USD", example="USD")
    method: str = Field(..., example="stripe")

    model_config = ConfigDict(from_attributes=True)

class PaymentConfirm(BaseModel):
    """
    Schema for confirming a payment.

    Attributes:
        token (str): The payment token received from the payment gateway,
                        used to confirm the transaction.
    """
    token: str = Field(..., example="tok_1Hx")

class PaymentStatus(BaseModel):
    """
    Schema for retrieving the status of a payment.

    Attributes:
        id (int): The unique identifier for the payment record.
        order_id (int): The ID of the order associated with this payment.
        user_id (int): The ID of the user who made the payment.
        status (str): The current status of the payment (e.g., "completed", "pending", "failed").
        transaction_id (Optional[str]): The ID of the transaction returned by the payment gateway, if applicable.
        created_at (datetime): The timestamp when the payment was created.
    """
    id: int
    order_id: int
    user_id: int
    status: str = Field(..., example="completed")
    transaction_id: Optional[str]
    created_at: datetime
