# app/db/base.py

"""
SQLAlchemy Declarative Base configuration.

This file defines the Base class used by all models in the application.
All models should inherit from Base to be correctly registered with SQLAlchemy.
Automatically includes created_at and updated_at timestamps.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all ORM models with automatic timestamping."""