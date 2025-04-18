"""
Restaurant Controller

Handles admin-level requests for creating, reading, updating, and deleting
restaurant branches or profiles. Delegates core logic to restaurant_service.
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_admin
from app.db.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantRead
from app.services import restaurant_service 


def create_restaurant_controller(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> RestaurantRead:
    """
    Create a new restaurant branch or profile.
    Role: Admin
    """
    return restaurant_service.create_restaurant(db, restaurant_data)


def get_restaurant_controller(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> RestaurantRead:
    """
    Retrieve a restaurant profile by its ID.
    Role: Admin
    """
    return restaurant_service.get_restaurant(db, restaurant_id)


def list_restaurants_controller(
    active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> List[RestaurantRead]:
    """
    List all restaurants. Optionally filter by active status.
    Role: Admin
    """
    return restaurant_service.list_restaurants(db, active)


def update_restaurant_controller(
    restaurant_id: int,
    update_data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> RestaurantRead:
    """
    Update an existing restaurant by ID.
    Role: Admin
    """
    return restaurant_service.update_restaurant(db, restaurant_id, update_data)


def delete_restaurant_controller(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> dict:
    """
    Delete a restaurant from the system.
    Role: Admin
    """
    return restaurant_service.delete_restaurant(db, restaurant_id)
