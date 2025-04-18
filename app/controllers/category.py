"""
Category Controller

Handles requests related to food category operations like creation, retrieval,
update, and deletion. Delegates business logic to the `category_service`.
"""

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_admin
from app.db.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from app.services import category_service


# Role : Admin
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> CategoryRead:
    """
    Create a new food category.

    Role: Admin
    """
    return category_service.create_category(db, category_data)



def list_categories(
    db: Session = Depends(get_db)
) -> List[CategoryRead]:
    """
    Retrieve all food categories.

    Role: Public
    """
    return category_service.list_categories(db)



def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db)
) -> CategoryRead:
    """
    Retrieve a single category by its ID.

    Role: Public
    """
    return category_service.get_category(db, category_id)


# Role : Admin
def update_category(
    category_id: int,
    update_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> CategoryRead:
    """
    Update an existing category's information.

    Role: Admin
    """
    return category_service.update_category(db, category_id, update_data)


# Role : Admin
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> dict:
    """
    Delete a category by its ID.

    Role: Admin
    """
    return category_service.delete_category(db, category_id)
