"""
Review and rating API routes.

This module provides RESTful API endpoints for managing user-submitted reviews
for restaurants and menu items. Users can:
- Submit reviews with ratings and comments
- Retrieve reviews by item, user, or ID
- Update existing reviews
- Delete reviews

All write operations require authentication.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.controllers import review as review_controller

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@cbv(router)
class ReviewAPI:
    """
    Class-based view for managing review-related routes.
    """
    db: Session = Depends(get_db)

    @router.post(
        "/",
        response_model=ReviewRead,
        status_code=status.HTTP_201_CREATED,
        summary="Create Review",
        response_description="The newly submitted review",
    )
    def create_review(
        self,
        review_data: ReviewCreate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Submit a new review.

        Args:
            review_data (ReviewCreate): Review input data from the client.
            current_user (User): Authenticated user submitting the review.

        Returns:
            ReviewRead: The created review record.

        Role: User
        """
        return review_controller.create_review(self.db, review_data, current_user.id)

    @router.get(
        "/menu-item/{item_id}",
        response_model=List[ReviewRead],
        status_code=status.HTTP_200_OK,
        summary="List Menu Item Reviews",
        response_description="Reviews for the specified menu item",
    )
    def list_reviews_for_item(self, item_id: int):
        """
        Retrieve all reviews for a specific menu item.

        Args:
            item_id (int): ID of the menu item to filter reviews.

        Returns:
            List[ReviewRead]: List of reviews.

        Role: Public
        """
        return review_controller.get_reviews_by_item(self.db, item_id)

    @router.get(
        "/user/{user_id}",
        response_model=List[ReviewRead],
        status_code=status.HTTP_200_OK,
        summary="List User Reviews",
        response_description="Reviews submitted by a specific user",
    )
    def list_reviews_by_user(
        self,
        user_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Retrieve all reviews submitted by a specific user.

        Args:
            user_id (int): User ID whose reviews are requested.
            current_user (User): Authenticated user performing the request.

        Returns:
            List[ReviewRead]: Reviews submitted by the user.

        Role: User
        """
        return review_controller.get_reviews_by_user(self.db, user_id)

    @router.get(
        "/{review_id}",
        response_model=ReviewRead,
        status_code=status.HTTP_200_OK,
        summary="Get Review",
        response_description="Detailed review by ID",
    )
    def get_review(self, review_id: int):
        """
        Retrieve a single review by its ID.

        Args:
            review_id (int): The ID of the review to retrieve.

        Returns:
            ReviewRead: The matching review.

        Role: Public
        """
        return review_controller.get_review(self.db, review_id)

    @router.put(
        "/{review_id}",
        response_model=ReviewRead,
        status_code=status.HTTP_200_OK,
        summary="Update Review",
        response_description="The updated review record",
    )
    def update_review(
        self,
        review_id: int,
        review_data: ReviewUpdate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Update an existing review.

        Args:
            review_id (int): ID of the review to be updated.
            review_data (ReviewUpdate): New review data (e.g., rating, comment).
            current_user (User): Authenticated user making the request.

        Returns:
            ReviewRead: The updated review record.

        Role: User
        """
        return review_controller.update_review(self.db, review_id, review_data, current_user.id)

    @router.delete(
        "/{review_id}",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Delete Review",
        response_description="Confirmation of review deletion",
    )
    def delete_review(
        self,
        review_id: int,
        current_user: User = Depends(get_current_user),
    ):
        """
        Delete a review by its ID.

        Args:
            review_id (int): The ID of the review to delete.
            current_user (User): Authenticated user requesting deletion.

        Returns:
            dict: Confirmation message.

        Role: User
        """
        return review_controller.delete_review(self.db, review_id, current_user.id)
