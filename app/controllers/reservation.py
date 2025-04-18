"""
Reservation Controller

Handles reservation-related user requests and delegates business logic
to the reservation_service module.

Roles:
- User: Can create, update, cancel, and view reservations
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationRead
from app.services import reservation_service


def create_reservation_controller(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Create a new table reservation.
    Role: User
    """
    return reservation_service.create_reservation(db, reservation_data, current_user.id)


def get_reservation_controller(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReservationRead:
    """
    Get a reservation by its ID.
    Role: User
    """
    return reservation_service.get_reservation(db, reservation_id, current_user.id)


def list_reservations_controller(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ReservationRead]:
    """
    List reservations. Optionally filter by user ID.
    Role: User
    """
    return reservation_service.list_reservations(db, user_id or current_user.id)


def update_reservation_controller(
    reservation_id: int,
    update_data: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReservationRead:
    """
    Update an existing reservation.
    Role: User
    """
    return reservation_service.update_reservation(db, reservation_id, update_data, current_user.id)


def cancel_reservation_controller(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Cancel an existing reservation.
    Role: User
    """
    return reservation_service.cancel_reservation(db, reservation_id, current_user.id)
