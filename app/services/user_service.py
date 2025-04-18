"""
User Service

Handles business logic for user profile management:
- View and update user profile
- List users (admin)
- Block or delete users (admin)
"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models.user import User
from app.schemas.user import UserUpdate


def list_users(db: Session) -> List[User]:
    """
    List all users in the system.

    Returns:
        List[User]: All registered users.
    """
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a user by their ID.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.

    Returns:
        User: The user object.

    Raises:
        HTTPException: If user is not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user_profile(db: Session, user_id: int, update_data: UserUpdate) -> User:
    """
    Update the profile of a user.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.
        update_data (UserUpdate): Fields to update.

    Returns:
        User: Updated user object.

    Raises:
        HTTPException: If user is not found.
    """
    user = get_user_by_id(db, user_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def block_user(db: Session, user_id: int) -> User:
    """
    Block or deactivate a user.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.

    Returns:
        User: Updated user object.
    """
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> dict:
    """
    Permanently delete a user from the system.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.

    Returns:
        dict: Deletion confirmation message.
    """
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
