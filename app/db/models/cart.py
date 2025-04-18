# app/db/models/cart.py

"""
Cart database model.

Represents items added to a user's shopping cart. Each cart item is associated with
a specific user and menu item, along with the desired quantity.
"""

from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class CartItem(Base):
    """
    Represents an item in a user's shopping cart.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user who owns this cart.
        menu_item_id (int): Foreign key to the menu item being added to the cart.
        quantity (int): Number of units of the menu item.
    """

    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint('user_id', 'menu_item_id', name='uq_user_menu_item'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Relationships
    user = relationship("User", back_populates="cart_items")
    menu_item = relationship("MenuItem", back_populates="cart_entries")
