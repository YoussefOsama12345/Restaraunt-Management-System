"""
api package

Defines the API package for the Restaurant Backend.
You can import and mount route modules from this package in the FastAPI application.
"""

"""
api package

Defines the API package for the Restaurant Backend.
You can import and mount route modules from this package in the FastAPI application.
"""

# Import all routers for easy mounting
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.categories import router as categories_router
from app.api.routes.menu_items import router as menu_items_router
from app.api.routes.cart import router as cart_router
from app.api.routes.orders import router as orders_router
from app.api.routes.reservations import router as reservations_router
from app.api.routes.restaurants import router as restaurants_router
from app.api.routes.deliveries import router as deliveries_router
from app.api.routes.payments import router as payments_router
from app.api.routes.addresses import router as addresses_router
from app.api.routes.support import router as support_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.notifications import router as notifications_router

__all__ = [
    "auth_router",
    "users_router",
    "categories_router",
    "menu_items_router",
    "cart_router",
    "orders_router",
    "reservations_router",
    "restaurants_router",
    "deliveries_router",
    "payments_router",
    "addresses_router",
    "support_router",
    "reviews_router",
    "inventory_router",
    "notifications_router",
]