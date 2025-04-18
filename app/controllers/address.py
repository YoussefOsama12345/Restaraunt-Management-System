"""
User Controller

Handles user-related operations such as profile retrieval, updates,
admin user management, blocking, and deletion.
Delegates business logic to user_service or directly accesses the DB via SQLAlchemy.
"""

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.db.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services import user_service


def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserRead:
    """
    Get the currently authenticated user's profile.
    Role: User
    """
    return user_service.get_user_profile(current_user)


def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Update the authenticated user's profile.
    Role: User
    """
    return user_service.update_user_profile(db, current_user.id, user_update)


def list_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> List[UserRead]:
    """
    List all registered users in the system.
    Role: Admin
    """
    return user_service.list_users(db)


def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> UserRead:
    """
    Get a user profile by their ID.
    Role: Admin
    """
    return user_service.get_user_by_id(db, user_id)


def block_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> UserRead:
    """
    Block or deactivate a user account.
    Role: Admin
    """
    return user_service.block_user(db, user_id)


def delete_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> dict:
    """
    Permanently delete a user account.
    Role: Admin
    """
    return user_service.delete_user(db, user_id)
