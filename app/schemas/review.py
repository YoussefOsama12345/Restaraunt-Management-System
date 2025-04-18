from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ReviewBase(BaseModel):
    """
    Base schema for review-related data.

    Attributes:
        menu_item_id (int): The ID of the menu item being reviewed.
        restaurant_id (Optional[int]): The ID of the restaurant being reviewed, if applicable.
        user_id (int): The ID of the user who submitted the review.
        rating (int): The rating given by the user (typically between 1 and 5).
        comment (Optional[str]): An optional comment provided by the user about the menu item or restaurant.
        created_at (datetime): The timestamp when the review was created.
    """
    menu_item_id: int
    restaurant_id: Optional[int] = None
    user_id: int
    rating: int = Field(..., ge=1, le=5, example=5)  # Rating must be between 1 and 5
    comment: Optional[str] = Field(None, example="Great taste!")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(ReviewBase):
    """
    Schema for creating a new review.

    Inherits from ReviewBase and is used to validate data when creating a new review.
    """
    pass

class ReviewUpdate(ReviewBase):
    """
    Schema for updating an existing review.

    Inherits from ReviewBase and is used to validate data when updating a review.
    """
    pass

class ReviewRead(ReviewBase):
    """
    Schema for returning review data to the client.

    Inherits from ReviewBase and includes additional fields for review identification.

    Attributes:
        id (int): The unique identifier for the review.
    """
    id: int
