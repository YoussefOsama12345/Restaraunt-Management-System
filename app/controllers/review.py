"""
Review Controller

Handles user interactions related to submitting, retrieving, updating,
and deleting reviews for menu items or restaurants. Delegates logic to
the review_service module.
"""

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.services import review_service


def create_review_controller(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReviewRead:
    """
    Submit a new review for a menu item or restaurant.
    Role: User
    """
    return review_service.create_review(db, review_data, current_user.id)


def list_reviews_for_item_controller(
    item_id: int,
    db: Session = Depends(get_db),
) -> List[ReviewRead]:
    """
    Get all reviews for a specific menu item.
    Role: Public
    """
    return review_service.list_reviews_for_item(db, item_id)


def list_reviews_by_user_controller(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ReviewRead]:
    """
    Get all reviews submitted by a specific user.
    Role: User
    """
    return review_service.list_reviews_by_user(db, user_id, current_user.id)


def get_review_controller(
    review_id: int,
    db: Session = Depends(get_db),
) -> ReviewRead:
    """
    Retrieve details of a single review by ID.
    Role: Public
    """
    return review_service.get_review(db, review_id)


def update_review_controller(
    review_id: int,
    update_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReviewRead:
    """
    Update an existing review's content or rating.
    Role: User
    """
    return review_service.update_review(db, review_id, update_data, current_user.id)


def delete_review_controller(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Delete a review by its ID.
    Role: User
    """
    return review_service.delete_review(db, review_id, current_user.id)
