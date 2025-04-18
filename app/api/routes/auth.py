"""
Authentication API routes.

Includes user login, registration, logout, password reset, and JWT-based authentication.
Supports email/password authentication and token refresh endpoints.
"""

import logging
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.controllers import auth as auth_controller 

router = APIRouter(prefix="/auth", tags=["auth"])

logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)


@cbv(router)
class AuthAPI:
    db: Session = Depends(get_db)

    @router.post(
        "/register",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        summary="Register User"
    )
    def register_user(self, user_data: UserCreate):
        """
        Register a new user with email and password.
        Role: Public
        """
        return auth_controller.register_user(user_data, self.db)

    @router.post(
        "/login",
        status_code=status.HTTP_200_OK,
        summary="User Login"
    )
    def login_user(self, credentials: UserCreate):
        """
        Login using email and password.
        Returns JWT token on success.
        Role: Public
        """
        return auth_controller.login_user(credentials.email, credentials.password, self.db)

    @router.post(
        "/logout",
        status_code=status.HTTP_200_OK,
        summary="Logout User"
    )
    def logout_user(self, current_user: User = Depends(get_current_user)):
        """
        Logout the current user.
        Role: User
        """
        return auth_controller.logout_user(current_user)

    @router.post(
        "/refresh",
        status_code=status.HTTP_200_OK,
        summary="Refresh Token"
    )
    def refresh_token(self, token: str):
        """
        Generate a new token using a valid refresh token.
        Role: Public
        """
        return auth_controller.refresh_token(token)

    @router.post(
        "/forgot-password",
        status_code=status.HTTP_202_ACCEPTED,
        summary="Forgot Password"
    )
    def forgot_password(self, email: str):
        """
        Send password reset instructions to email.
        Role: Public
        """
        return auth_controller.forgot_password(email, self.db)

    @router.post(
        "/reset-password",
        status_code=status.HTTP_200_OK,
        summary="Reset Password"
    )
    def reset_password(self, token: str, new_password: str):
        """
        Reset password using a valid token.
        Role: Public
        """
        return auth_controller.reset_password(token, new_password, self.db)
