"""
Support Ticket Controller

Manages customer support ticket interactions including creation,
retrieval, updating status, posting replies, and deletion.
Delegates logic to support_service.
"""

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.support_ticket import (
    SupportTicketCreate,
    SupportTicketRead,
    SupportTicketReply,
)
from app.services import support_service


def create_support_ticket_controller(
    ticket_data: SupportTicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SupportTicketRead:
    """
    Create a new support ticket related to an order or reservation.
    Role: User
    """
    return support_service.create_ticket(db, ticket_data, current_user.id)


def get_support_ticket_controller(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SupportTicketRead:
    """
    Get full details for a single ticket, including messages and status.
    Role: User
    """
    return support_service.get_ticket(db, ticket_id, current_user.id)


def list_support_tickets_by_user_controller(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[SupportTicketRead]:
    """
    Get all support tickets submitted by the user.
    Role: User
    """
    return support_service.list_tickets_by_user(db, user_id, current_user.id)


def update_ticket_status_controller(
    ticket_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SupportTicketRead:
    """
    Update the status of a support ticket.
    Role: User or Admin
    """
    return support_service.update_ticket_status(db, ticket_id, new_status, current_user.id)


def reply_to_ticket_controller(
    ticket_id: int,
    reply_data: SupportTicketReply,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SupportTicketRead:
    """
    Append a reply to the conversation thread of a support ticket.
    Role: User
    """
    return support_service.reply_to_ticket(db, ticket_id, reply_data, current_user.id)


def close_ticket_controller(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Close a support ticket and optionally archive it.
    Role: User
    """
    return support_service.close_ticket(db, ticket_id, current_user.id)
