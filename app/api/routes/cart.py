"""
Shopping cart API routes.

Provides endpoints for managing a user's shopping cart, including adding items,
viewing cart contents, updating item quantities, and clearing the cart.
All routes require authenticated user access.
"""

import logging
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.cart import CartItemCreate, CartItemRead
from app.controllers import cart as cart_controller  

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    dependencies=[Depends(get_current_user)],
)

logger = logging.getLogger("cart")
logger.setLevel(logging.INFO)


@cbv(router)
class CartAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=CartItemRead,
        status_code=status.HTTP_201_CREATED,
        summary="Add Item to Cart",
        response_description="Item successfully added to cart",
    )
    def add_item_to_cart(
        self,
        address_data: CartItemCreate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Add an item to the authenticated user's shopping cart.
        Role: User
        """
        return cart_controller.add_item_to_cart(address_data, self.db, current_user)

    @router.get(
        "/",
        response_model=List[CartItemRead],
        status_code=status.HTTP_200_OK,
        summary="Get Cart Items",
        response_description="All items in the user's cart",
    )
    def get_cart(
        self,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve all items in the authenticated user's shopping cart.
        Role: User
        """
        return cart_controller.get_cart_items(self.db, current_user)

    @router.put(
        "/{cart_item_id}",
        response_model=CartItemRead,
        status_code=status.HTTP_200_OK,
        summary="Update Cart Item",
        response_description="Updated cart item with new quantity",
    )
    def update_cart_item(
        self,
        cart_item_id: int,
        quantity: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Update the quantity of a specific item in the cart.
        Role: User
        """
        return cart_controller.update_cart_item(cart_item_id, quantity, self.db, current_user)

    @router.delete(
        "/{cart_item_id}",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Remove Cart Item",
        response_description="Confirmation of item removal from cart",
    )
    def remove_cart_item(
        self,
        cart_item_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Remove a specific item from the authenticated user's cart.
        Role: User
        """
        return cart_controller.remove_cart_item(cart_item_id, self.db, current_user)

    @router.delete(
        "/",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Clear Cart",
        response_description="All items removed from user's cart",
    )
    def clear_cart(
        self,
        current_user: User = Depends(get_current_user),
    ):
        """
        Clear all items from the authenticated user's shopping cart.
        Role: User
        """
        return cart_controller.clear_user_cart(self.db, current_user)
