"""
User address book API routes.

Provides endpoints for authenticated users to manage delivery and billing addresses.
Supports creation, retrieval, updating, and deletion of address records,
enabling multi-address accounts for flexible deliveries.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.address import AddressCreate, AddressRead, AddressUpdate
from app.controllers import address as address_controller  

router = APIRouter(prefix="/addresses", tags=["addresses"])

logger = logging.getLogger("address")
logger.setLevel(logging.INFO)


@cbv(router)
class AddressAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=AddressRead,
        status_code=status.HTTP_201_CREATED,
        summary="Create Address",
        response_description="The newly created address",
    )
    def create_address(
        self,
        address_data: AddressCreate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Create a new delivery or billing address for the authenticated user.
        Role: User
        """
        return address_controller.create_address(address_data, self.db, current_user)

    @router.get(
        "/",
        response_model=List[AddressRead],
        status_code=status.HTTP_200_OK,
        summary="List Addresses",
        response_description="All saved addresses for the user",
    )
    def get_user_addresses(
        self,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve all saved addresses for the authenticated user.
        Role: User
        """
        return address_controller.get_user_addresses(self.db, current_user)

    @router.put(
        "/{address_id}",
        response_model=AddressRead,
        status_code=status.HTTP_200_OK,
        summary="Update Address",
        response_description="The updated address record",
    )
    def update_address(
        self,
        address_id: int,
        address_data: AddressUpdate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Update an existing address by its ID for the authenticated user.
        Role: User
        """
        return address_controller.update_address(address_id, address_data, self.db, current_user)

    @router.delete(
        "/{address_id}",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Delete Address",
        response_description="Confirmation of address deletion",
    )
    def delete_address(
        self,
        address_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Delete a saved address by its ID for the authenticated user.
        Role: User
        """
        return address_controller.delete_address(address_id, self.db, current_user)

    @router.get(
        "/default",
        response_model=AddressRead,
        status_code=status.HTTP_200_OK,
        summary="Get Default Address",
        response_description="The user's default address",
    )
    def get_default_address(
        self,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve the default address for the authenticated user.
        Role: User
        """
        return address_controller.get_default_address(self.db, current_user)
