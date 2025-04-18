"""
Support ticket API routes.

Allows users to submit support tickets, view their ticket history,
and allows admin users to respond or change ticket status.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.db.models.user import User
from app.schemas.support_ticket import SupportTicketCreate, SupportTicketRead, SupportTicketUpdate
from app.controllers import support_ticket as support_controller

router = APIRouter(prefix="/support", tags=["support"])


@cbv(router)
class SupportAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=SupportTicketRead,
        status_code=status.HTTP_201_CREATED,
        summary="Create Support Ticket",
        response_description="The newly created support ticket",
    )
    def create_ticket(
        self,
        ticket_data: SupportTicketCreate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Submit a new support ticket.

        Users can submit issues or questions regarding orders, reservations, or general inquiries.
        Role: User
        """
        return support_controller.create_ticket(self.db, ticket_data, current_user.id)

    @router.get(
        "/",
        response_model=List[SupportTicketRead],
        status_code=status.HTTP_200_OK,
        summary="List User Tickets",
        response_description="All support tickets submitted by the current user",
    )
    def list_user_tickets(
        self,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve all tickets submitted by the authenticated user.

        Role: User
        """
        return support_controller.get_user_tickets(self.db, current_user.id)

    @router.get(
        "/all",
        response_model=List[SupportTicketRead],
        status_code=status.HTTP_200_OK,
        summary="List All Tickets (Admin)",
        response_description="All support tickets submitted in the system",
        dependencies=[Depends(get_current_admin)],
    )
    def list_all_tickets(
        self,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Admin-only endpoint to list all submitted support tickets.

        Role: Admin
        """
        return support_controller.get_all_tickets(self.db)

    @router.get(
        "/{ticket_id}",
        response_model=SupportTicketRead,
        status_code=status.HTTP_200_OK,
        summary="Get Ticket",
        response_description="Details of a specific support ticket",
    )
    def get_ticket(
        self,
        ticket_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Get details of a specific support ticket by its ID.

        Role: User
        """
        return support_controller.get_ticket(self.db, ticket_id, current_user.id)

    @router.put(
        "/{ticket_id}",
        response_model=SupportTicketRead,
        status_code=status.HTTP_200_OK,
        summary="Update Ticket (Admin)",
        response_description="The updated ticket record",
        dependencies=[Depends(get_current_admin)],
    )
    def update_ticket(
        self,
        ticket_id: int,
        update_data: SupportTicketUpdate,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Admin-only endpoint to update the status or reply of a ticket.

        Role: Admin
        """
        return support_controller.update_ticket(self.db, ticket_id, update_data)
