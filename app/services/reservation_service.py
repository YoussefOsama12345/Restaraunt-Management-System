"""
Reservation service for handling table booking operations.

Includes:
- Creating new reservations
- Fetching individual reservation details
- Listing all or user-specific reservations
- Updating reservation details
- Canceling reservations

All operations require user context and specific roles.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate

# Role : User

def create_reservation(db: Session, reservation_data: ReservationCreate, user_id: int) -> Reservation:
    """
    Create a new table reservation.

    Role: User

    Args:
        db (Session): Database session.
        reservation_data (ReservationCreate): Input data for the reservation.
        user_id (int): ID of the authenticated user creating the reservation.

    Returns:
        Reservation: Newly created reservation object.

    Raises:
        HTTPException: If reservation cannot be created (e.g., conflicts, invalid data).
    """
    pass

# Role : User

def get_reservation(db: Session, reservation_id: int, user_id: int) -> Reservation:
    """
    Retrieve a specific reservation by ID.

    Role: User

    Args:
        db (Session): Database session.
        reservation_id (int): Reservation ID to retrieve.
        user_id (int): ID of the requesting user.

    Returns:
        Reservation: Reservation object with full details.

    Raises:
        HTTPException: If not found or user unauthorized to access.
    """
    pass

# Role : User

def list_reservations(db: Session, user_id: Optional[int] = None) -> List[Reservation]:
    """
    List reservations, optionally filtered by user.

    Role: User

    Args:
        db (Session): Database session.
        user_id (int, optional): User ID to filter by (None = all).

    Returns:
        List[Reservation]: List of reservation records.
    """
    pass


# Role : User

def update_reservation(
    db: Session,
    reservation_id: int,
    update_data: ReservationUpdate,
    user_id: int
) -> Reservation:
    """
    Update an existing reservation's data.

    Role: User

    Args:
        db (Session): Database session.
        reservation_id (int): ID of the reservation to update.
        update_data (ReservationUpdate): Updated fields.
        user_id (int): ID of the user performing the update.

    Returns:
        Reservation: Updated reservation object.

    Raises:
        HTTPException: If reservation not found or access denied.
    """
    pass


# Role : User

def cancel_reservation(db: Session, reservation_id: int, user_id: int) -> dict:
    """
    Cancel a reservation by marking it as 'cancelled'.

    Role: User

    Args:
        db (Session): Database session.
        reservation_id (int): ID of the reservation to cancel.
        user_id (int): ID of the user cancelling it.

    Returns:
        dict: Confirmation response.

    Raises:
        HTTPException: If reservation is invalid or access is denied.
    """
    pass
