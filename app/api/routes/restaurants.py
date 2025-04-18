"""
Restaurant Management API Routes.

Provides endpoints for managing restaurant details and metadata.
Supports viewing, creating, updating, and deleting restaurants.
"""

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.deps import get_current_admin
from app.db.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantRead
from app.controllers import restaurant as restaurant_controller

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)

@cbv(router)
class RestaurantAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=RestaurantRead,
        status_code=status.HTTP_201_CREATED,
        summary="Create Restaurant",
        description="Create a new restaurant entry (Admin only)",
        dependencies=[Depends(get_current_admin)],
    )
    def create_restaurant(
        self,
        restaurant_data: RestaurantCreate,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Add a new restaurant entry to the system.
        Role: Admin
        """
        return restaurant_controller.create_restaurant(self.db, restaurant_data)

    @router.get(
        "/",
        response_model=List[RestaurantRead],
        status_code=status.HTTP_200_OK,
        summary="List Restaurants",
        description="Get all available restaurants",
    )
    def list_restaurants(self):
        """
        Retrieve a list of all available restaurants.
        Role: Public
        """
        return restaurant_controller.list_restaurants(self.db)

    @router.get(
        "/{restaurant_id}",
        response_model=RestaurantRead,
        status_code=status.HTTP_200_OK,
        summary="Get Restaurant",
        description="Get detailed information for a specific restaurant",
    )
    def get_restaurant(self, restaurant_id: int):
        """
        Retrieve information about a single restaurant by ID.
        Role: Public
        """
        return restaurant_controller.get_restaurant(self.db, restaurant_id)

    @router.put(
        "/{restaurant_id}",
        response_model=RestaurantRead,
        status_code=status.HTTP_200_OK,
        summary="Update Restaurant",
        description="Update the information of a restaurant (Admin only)",
        dependencies=[Depends(get_current_admin)],
    )
    def update_restaurant(
        self,
        restaurant_id: int,
        update_data: RestaurantUpdate,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Update restaurant metadata such as name, location, or contact info.
        Role: Admin
        """
        return restaurant_controller.update_restaurant(self.db, restaurant_id, update_data)

    @router.delete(
        "/{restaurant_id}",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Delete Restaurant",
        description="Delete a restaurant entry (Admin only)",
        dependencies=[Depends(get_current_admin)],
    )
    def delete_restaurant(
        self,
        restaurant_id: int,
        current_user: User = Depends(get_current_admin),
    ):
        """
        Delete a restaurant from the system by ID.
        Role: Admin
        """
        return restaurant_controller.delete_restaurant(self.db, restaurant_id)
