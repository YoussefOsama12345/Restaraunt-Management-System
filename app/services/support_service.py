"""
Support Service

Handles logic for customer support ticket operations:

- Submitting new support tickets
- Viewing user-specific or individual ticket details
- Updating ticket status
- Replying to tickets (user/agent)
- Deleting/closing tickets

Roles:
- User (submit, view own, reply)
- Admin (view all, update status, delete)
"""

from typing import List
from sqlalchemy.orm import Session
from app.db.models import SupportTicket
from app.schemas.support_ticket import SupportTicketCreate, SupportTicketUpdate, SupportReplyCreate


def create_support_ticket(db: Session, ticket_data: SupportTicketCreate, user_id: int) -> SupportTicket:
    """
    Submit a new support ticket.

    Args:
        db (Session): Database session.
        ticket_data (SupportTicketCreate): Info about the issue.
        user_id (int): ID of the user submitting the ticket.

    Returns:
        SupportTicket: The created support ticket.

    Role: User
    """
    pass


def get_support_ticket(db: Session, ticket_id: int, user_id: int, is_admin: bool = False) -> SupportTicket:
    """
    Retrieve a specific support ticket by ID.

    Args:
        db (Session): Database session.
        ticket_id (int): ID of the ticket.
        user_id (int): ID of the requesting user.
        is_admin (bool): Whether the requester is an admin.

    Returns:
        SupportTicket: The requested support ticket.

    Role: User (own), Admin (any)
    """
    pass


def list_support_tickets_by_user(db: Session, user_id: int) -> List[SupportTicket]:
    """
    List all support tickets submitted by a specific user.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.

    Returns:
        List[SupportTicket]: User's support tickets.

    Role: User
    """
    pass


def list_all_support_tickets(db: Session) -> List[SupportTicket]:
    """
    List all support tickets in the system.

    Args:
        db (Session): Database session.

    Returns:
        List[SupportTicket]: All support tickets.

    Role: Admin
    """
    pass


def update_ticket_status(db: Session, ticket_id: int, status: str, admin_id: int) -> SupportTicket:
    """
    Update the status of a support ticket.

    Args:
        db (Session): Database session.
        ticket_id (int): Ticket to update.
        status (str): New status ('open', 'in_progress', 'resolved', etc.).
        admin_id (int): Admin performing the update.

    Returns:
        SupportTicket: Updated ticket.

    Role: Admin
    """
    pass


def reply_to_ticket(db: Session, ticket_id: int, reply_data: SupportReplyCreate, sender_id: int, is_admin: bool) -> dict:
    """
    Post a reply to a support ticket.

    Args:
        db (Session): Database session.
        ticket_id (int): Ticket being replied to.
        reply_data (SupportReplyCreate): Reply content.
        sender_id (int): ID of user/admin sending the reply.
        is_admin (bool): Whether the sender is admin.

    Returns:
        dict: Confirmation message.

    Role: User or Admin
    """
    pass


def delete_ticket(db: Session, ticket_id: int, admin_id: int) -> dict:
    """
    Delete or close a support ticket.

    Args:
        db (Session): Database session.
        ticket_id (int): Ticket to delete/close.
        admin_id (int): Admin performing the action.

    Returns:
        dict: Confirmation message.

    Role: Admin
    """
    pass
