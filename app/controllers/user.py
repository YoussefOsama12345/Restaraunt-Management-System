"""
User Controller

Handles business logic for managing user accounts:
- List users (admin)
- Get/update personal profile
- Get user by ID (admin)
- Block or delete user accounts

Delegates logic to user_service.
"""

from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.api.deps import get_current_user, get_current_admin
from app.services import user_service

def list_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> List[UserRead]:
    """
    List all users in the system.
    Role: Admin
    """
    return user_service.list_users(db)

def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Get the currently authenticated user's profile.
    Role: User
    """
    return user_service.get_user_profile(current_user)

def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Update fields in the current user's profile.
    Role: User
    """
    return user_service.update_user_profile(db, current_user, user_update)

def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> UserRead:
    """
    Retrieve a specific user's profile by ID.
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
    Permanently delete a user account by ID.
    Role: Admin
    """
    return user_service.delete_user(db, user_id)
