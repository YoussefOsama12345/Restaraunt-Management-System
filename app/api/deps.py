"""
Defines common dependencies for API endpoints, including:
- Database session (get_db)
- OAuth2 password bearer token scheme
- Current user retrieval and role-based access control
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User, UserRole
from app.security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieve the current authenticated user based on JWT token.

    Raises HTTP 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: int = int(payload.get("sub"))
    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
    return user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that ensures the current user has admin privileges.

    Raises HTTP 403 if user is not an admin.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def get_current_delivery(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that ensures the current user has delivery staff privileges.

    Raises HTTP 403 if user is not delivery personnel.
    """
    if current_user.role != UserRole.delivery:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Delivery privileges required"
        )
    return current_user
