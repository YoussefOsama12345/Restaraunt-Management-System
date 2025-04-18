"""
Schemas for managing support tickets in the application.

This module defines the data models used for creating, updating, and retrieving support tickets.
It includes the following schemas:
- SupportTicketBase: Base schema for common ticket attributes.
- SupportTicketCreate: Schema for creating a new support ticket.
- SupportTicketUpdate: Schema for updating an existing support ticket.
- SupportTicketRead: Schema for returning ticket data to the client.

Each schema uses Pydantic for data validation and serialization.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SupportTicketBase(BaseModel):
    """
    Base schema for support ticket-related data.

    Attributes:
        user_id (int): The ID of the user submitting the ticket.
        subject (str): The subject of the support ticket.
        message (str): The detailed message describing the issue.
        order_id (Optional[int]): The ID of the related order, if applicable.
        reservation_id (Optional[int]): The ID of the related reservation, if applicable.
        created_at (datetime): The timestamp when the ticket was created.
        status (str): The current status of the ticket (e.g., "open", "in_progress", "resolved").
    """
    user_id: int
    subject: str = Field(..., example="Issue with my order")
    message: str = Field(..., example="I received the wrong item.")
    order_id: Optional[int] = None
    reservation_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field("open", example="open")

    model_config = ConfigDict(from_attributes=True)

class SupportTicketCreate(SupportTicketBase):
    """
    Schema for creating a new support ticket.

    Inherits from SupportTicketBase and is used to validate data when creating a new ticket.
    This schema ensures that all required fields are provided for ticket creation.
    """
    pass

class SupportTicketUpdate(SupportTicketBase):
    """
    Schema for updating an existing support ticket.

    Inherits from SupportTicketBase and is used to validate data when updating a ticket.
    This schema allows modification of fields such as subject, message, and status.
    """
    pass

class SupportTicketRead(SupportTicketBase):
    """
    Schema for returning support ticket data to the client.

    Inherits from SupportTicketBase and includes additional fields for ticket identification.

    Attributes:
        id (int): The unique identifier for the support ticket.
    """
    id: int
