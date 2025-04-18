"""
Auth Controller

Handles HTTP request-level logic for registration, login, token handling, and Firebase auth.
Delegates core logic to the `auth_service`.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import UserCreate
from app.services import auth_service
from app.db.models.user import User


def register_user(user_data: UserCreate, db: Session) -> User:
    """
    Controller for registering a new user with email/password.
    """
    return auth_service.register_user(db, user_data)


def login_user(email: str, password: str, db: Session) -> str:
    """
    Controller for logging in with email and password.
    Returns JWT token if successful.
    """
    user = auth_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return auth_service.create_access_token({"sub": user.email})


def login_with_oauth(firebase_token: str, db: Session) -> str:
    """
    Controller for logging in via Firebase OAuth (Google/Facebook).
    """
    firebase_data = auth_service.verify_oauth_token(firebase_token)
    user = auth_service.login_or_register_oauth(db, firebase_data)
    return auth_service.create_access_token({"sub": user.email})


def refresh_token(token: str) -> str:
    """
    Controller for refreshing access token from a valid refresh token.
    """
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return auth_service.create_access_token({"sub": payload.get("sub")})
