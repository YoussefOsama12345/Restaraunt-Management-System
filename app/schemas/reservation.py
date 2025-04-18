from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ReservationBase(BaseModel):
    """
    Base schema for reservation-related data.

    Attributes:
        reservation_time (datetime): The date and time of the reservation.
        guests (int): The number of guests for the reservation.
        table_number (Optional[int]): The table number assigned to the reservation, if applicable.
        special_request (Optional[str]): Any special requests made by the user (e.g., "Window seat, please").
    """
    reservation_time: datetime
    guests: int
    table_number: Optional[int] = None
    special_request: Optional[str] = Field(None, example="Window seat, please")

    model_config = ConfigDict(from_attributes=True)

class ReservationCreate(ReservationBase):
    """
    Schema for creating a new reservation.

    Inherits from ReservationBase and is used to validate data when creating a new reservation.
    """
    pass

class ReservationUpdate(ReservationBase):
    """
    Schema for updating an existing reservation.

    Inherits from ReservationBase and is used to validate data when updating a reservation.
    """
    pass

class ReservationRead(ReservationBase):
    """
    Schema for returning reservation data to the client.

    Inherits from ReservationBase and includes additional fields for reservation identification.

    Attributes:
        id (int): The unique identifier for the reservation.
        user_id (int): The ID of the user who made the reservation.
        status (str): The current status of the reservation (e.g., "confirmed", "canceled").
        created_at (datetime): The timestamp when the reservation was created.
    """
    id: int
    user_id: int
    status: str = Field(..., example="confirmed")
    created_at: datetime