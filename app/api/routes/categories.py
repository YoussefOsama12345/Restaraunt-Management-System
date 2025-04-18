"""
Address Controller

Manages address book operations for authenticated users, including:
- Creating new addresses
- Listing saved addresses
- Updating existing addresses
- Deleting addresses
- Retrieving the default address

Delegates business logic to address_service.

Access: All endpoints require authenticated users.
"""

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.address import AddressCreate, AddressUpdate, AddressRead
from app.services import address_service 


# Role: User
def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressRead:
    """
    Create a new delivery or billing address.

    Args:
        address_data (AddressCreate): Address input details.
        db (Session): Active DB session.
        current_user (User): The authenticated user.

    Returns:
        AddressRead: The newly created address object.
    """
    return address_service.create_address(db, address_data, current_user.id)


# Role: User
def get_user_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[AddressRead]:
    """
    Retrieve all addresses saved by the user.

    Args:
        db (Session): Active DB session.
        current_user (User): The authenticated user.

    Returns:
        List[AddressRead]: All saved addresses for the user.
    """
    return address_service.list_addresses(db, current_user.id)


# Role: User
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressRead:
    """
    Update an existing address by its ID.

    Args:
        address_id (int): ID of the address to update.
        address_data (AddressUpdate): Updated field values.
        db (Session): Active DB session.
        current_user (User): The authenticated user.

    Returns:
        AddressRead: The updated address object.
    """
    return address_service.update_address(db, address_id, address_data, current_user.id)


# Role: User
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Delete an address from the user's account.

    Args:
        address_id (int): ID of the address to delete.
        db (Session): Active DB session.
        current_user (User): The authenticated user.

    Returns:
        dict: Confirmation of deletion.
    """
    return address_service.delete_address(db, address_id, current_user.id)


# Role: User
def get_default_address(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressRead:
    """
    Retrieve the default address for the user.

    Args:
        db (Session): Active DB session.
        current_user (User): The authenticated user.

    Returns:
        AddressRead: The default address, if available.
    """
    return address_service.get_default_address(db, current_user.id)
