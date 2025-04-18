"""
Cart Controller

Handles user requests related to shopping cart operations and delegates
business logic to the cart_service module.

This module performs the following operations:
- Add items to cart
- Retrieve user's cart items
- Update item quantity in cart
- Remove an item from cart
- Clear all items from cart

Access: All endpoints require the user to be authenticated.
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.cart import CartItemCreate, CartItemRead
from app.services import cart_service


# Role: User
def add_item_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CartItemRead:
    """
    Add a new item to the user's cart.

    Args:
        item_data (CartItemCreate): Details of the menu item and quantity.
        db (Session): Active database session.
        current_user (User): The currently authenticated user.

    Returns:
        CartItemRead: The added cart item record.

    Role: User
    """
    return cart_service.add_to_cart(db, item_data, current_user.id)


# Role: User
def get_cart_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[CartItemRead]:
    """
    Retrieve all items currently in the authenticated user's cart.

    Args:
        db (Session): Active database session.
        current_user (User): The currently authenticated user.

    Returns:
        List[CartItemRead]: A list of cart items for the user.

    Role: User
    """
    return cart_service.get_user_cart(db, current_user.id)


# Role: User
def update_cart_item(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CartItemRead:
    """
    Update the quantity of a specific cart item.

    Args:
        cart_item_id (int): ID of the cart item to update.
        quantity (int): New quantity to set.
        db (Session): Active database session.
        current_user (User): The currently authenticated user.

    Returns:
        CartItemRead: The updated cart item record.

    Role: User
    """
    return cart_service.update_cart_quantity(db, cart_item_id, quantity, current_user.id)


# Role: User
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Remove an item from the user's cart.

    Args:
        cart_item_id (int): ID of the cart item to remove.
        db (Session): Active database session.
        current_user (User): The currently authenticated user.

    Returns:
        dict: Confirmation message on deletion.

    Role: User
    """
    return cart_service.remove_item_from_cart(db, cart_item_id, current_user.id)


# Role: User
def clear_user_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Clear all items from the user's cart.

    Args:
        db (Session): Active database session.
        current_user (User): The currently authenticated user.

    Returns:
        dict: Confirmation message on cart clearance.

    Role: User
    """
    return cart_service.clear_cart(db, current_user.id)
