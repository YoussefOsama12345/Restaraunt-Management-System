
"""
Reservation booking API routes.

Manages table reservations with support for creating, retrieving, listing,
updating, and canceling reservations, including guest count and special requests.
All endpoints require user authentication.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationRead
from app.controllers import reservation as reservation_controller

router = APIRouter(prefix="/reservations", tags=["reservations"])

@cbv(router)
class ReservationAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=dict,
        status_code=status.HTTP_201_CREATED,
        summary="Create Reservation",
        description="Create a new reservation with guest count, date, time, and special requests."
    )
    def create_reservation(
        self,
        reservation_data: ReservationCreate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Create a new table reservation.

        Accepts details such as user_id, date, time, number of guests,
        table preferences, and special requests, then stores the reservation.
        Role: User
        """
        return reservation_controller.create_reservation(self.db, reservation_data, current_user.id)

    @router.get(
        "/{reservation_id}",
        response_model=ReservationRead,
        status_code=status.HTTP_200_OK,
        summary="Get Reservation",
        description="Retrieve a specific reservation's details by ID.",
    )
    def get_reservation(
        self,
        reservation_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve detailed information for a specific reservation by ID.

        Returns reservation details including date, time, guests, and status.
        Role: User
        """
        return reservation_controller.get_reservation(self.db, reservation_id, current_user.id)

    @router.get(
        "/",
        response_model=List[ReservationRead],
        status_code=status.HTTP_200_OK,
        summary="List Reservations",
        description="List all reservations or filter by user ID.",
    )
    def list_reservations(
        self,
        user_id: Optional[int] = None,
        current_user: User = Depends(get_current_user),
    ):
        """
        List reservations, optionally filtered by user ID.

        Returns all reservations or those belonging to a specific user.
        Role: User
        """
        return reservation_controller.list_reservations(self.db, user_id or current_user.id)

    @router.put(
        "/{reservation_id}",
        response_model=ReservationRead,
        status_code=status.HTTP_200_OK,
        summary="Update Reservation",
        description="Update a reservation's date, guest count, or special notes.",
    )
    def update_reservation(
        self,
        reservation_id: int,
        reservation_data: ReservationUpdate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Update an existing reservation by ID.

        Allows modification of date, time, guest count, and special requests.
        Role: User
        """
        return reservation_controller.update_reservation(self.db, reservation_id, reservation_data, current_user.id)

    @router.post(
        "/{reservation_id}/cancel",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Cancel Reservation",
        description="Cancel a reservation and optionally notify the user.",
    )
    def cancel_reservation(
        self,
        reservation_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Cancel an existing reservation by ID.

        Marks the reservation as canceled and notifies the user if necessary.
        Role: User
        """
        return reservation_controller.cancel_reservation(self.db, reservation_id, current_user.id)

