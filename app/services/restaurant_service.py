"""
Restaurant Service

Provides business logic for managing restaurant information including
creation, updates, retrieval, deletion, and optional search/filter functionality.

Use Cases:
- Admins can create and manage restaurants
- Public users can view/search restaurants
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def create_restaurant(db: Session, data: RestaurantCreate) -> Restaurant:
    """
    Create a new restaurant entry.

    Args:
        db (Session): Database session
        data (RestaurantCreate): Restaurant data input

    Returns:
        Restaurant: Created restaurant object
    """
    existing = db.query(Restaurant).filter(Restaurant.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant already exists")

    restaurant = Restaurant(**data.dict())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurant(db: Session, restaurant_id: int) -> Restaurant:
    """
    Retrieve a restaurant by ID.

    Args:
        db (Session): Database session
        restaurant_id (int): ID of the restaurant

    Returns:
        Restaurant: Found restaurant object
    """
    restaurant = db.query(Restaurant).get(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


def list_restaurants(db: Session) -> List[Restaurant]:
    """
    List all available restaurants.

    Args:
        db (Session): Database session

    Returns:
        List[Restaurant]: All restaurant records
    """
    return db.query(Restaurant).all()


def update_restaurant(db: Session, restaurant_id: int, data: RestaurantUpdate) -> Restaurant:
    """
    Update a restaurant's details.

    Args:
        db (Session): Database session
        restaurant_id (int): ID of the restaurant
        data (RestaurantUpdate): Fields to update

    Returns:
        Restaurant: Updated restaurant object
    """
    restaurant = get_restaurant(db, restaurant_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def delete_restaurant(db: Session, restaurant_id: int) -> dict:
    """
    Delete a restaurant entry.

    Args:
        db (Session): Database session
        restaurant_id (int): ID of the restaurant

    Returns:
        dict: Deletion confirmation message
    """
    restaurant = get_restaurant(db, restaurant_id)
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"}


def search_restaurants(db: Session, query: str) -> List[Restaurant]:
    """
    Search restaurants by name or location.

    Args:
        db (Session): Database session
        query (str): Search keyword

    Returns:
        List[Restaurant]: Matched restaurants
    """
    return db.query(Restaurant).filter(
        (Restaurant.name.ilike(f"%{query}%")) |
        (Restaurant.address.ilike(f"%{query}%"))
    ).all()
