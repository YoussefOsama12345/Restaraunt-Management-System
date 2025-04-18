"""
Handles operations related to user accounts, including retrieval of user profiles,
updating user information, listing users (admin-only), and managing account status.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserRead, UserUpdate
from app.api.deps import get_current_user, get_current_admin
from app.db.models.user import User
from app.controllers import user as user_controller  

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class UserAPI:
    db: Session = Depends(get_db)

    @router.get(
        "/",
        response_model=List[UserRead],
        status_code=status.HTTP_200_OK,
        summary="List All Users",
        description="Admin-only route to retrieve a list of all registered users with profile info.",
        dependencies=[Depends(get_current_admin)],
    )
    def list_users(self):
        """
        List all registered users.
        Role: Admin
        """
        return user_controller.list_users(self.db)

    @router.get(
        "/me",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        summary="Get Current User",
        description="Returns the profile data of the currently authenticated user."
    )
    def get_my_profile(self, current_user: User = Depends(get_current_user)):
        """
        Get the profile of the currently authenticated user.
        Role: User
        """
        return user_controller.get_my_profile(self.db, current_user.id)

    @router.put(
        "/me",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        summary="Update My Profile",
        description="Update personal profile data for the currently authenticated user (e.g., full name, phone)."
    )
    def update_my_profile(
        self,
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user),
    ):
        """
        Update the authenticated user's profile.
        Role: User
        """
        return user_controller.update_my_profile(self.db, current_user.id, user_update)

    @router.get(
        "/{user_id}",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        summary="Get User by ID",
        description="Fetch a specific user's profile using their user ID (admin only).",
        dependencies=[Depends(get_current_admin)],
    )
    def get_user_by_id(self, user_id: int, current_user: User = Depends(get_current_user)):
        """
        Retrieve a specific user's profile by user ID.
        Role: Admin
        """
        return user_controller.get_user_by_id(self.db, user_id)

    @router.put(
        "/{user_id}/block",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        summary="Block User",
        description="Temporarily block or deactivate a user account by ID (admin only).",
        dependencies=[Depends(get_current_admin)],
    )
    def block_user(self, user_id: int, current_user: User = Depends(get_current_admin)):
        """
        Block a user account by user ID.
        Role: Admin
        """
        return user_controller.block_user(self.db, user_id)

    @router.delete(
        "/{user_id}",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Delete User",
        description="Permanently delete a user account by ID (admin only).",
        dependencies=[Depends(get_current_admin)],
    )
    def delete_user(self, user_id: int, current_user: User = Depends(get_current_user)):
        """
        Delete a user account by user ID.
        Role: Admin
        """
        return user_controller.delete_user(self.db, user_id)

    @router.get(
        "/profile",
        response_model=dict,
        status_code=status.HTTP_200_OK,
        summary="Current User Profile",
        description="Returns the current authenticated user's basic metadata (e.g., username)."
    )
    def get_user_profile(self, current_user: User = Depends(get_current_user)):
        """
        Get the profile of the currently authenticated user.
        Role: User
        """
        return {"username": current_user.email}
