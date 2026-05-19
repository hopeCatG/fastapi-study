from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.models.user_model import User
from app.schemas.user_schema import UserRead, UserCreate, UserUpdate
from .backend import auth_backend
from .manager import get_user_manager

# FastAPIUsers instance: the core of the library
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# --- Routers ---

# Router for authentication (login, logout)
auth_router = fastapi_users.get_auth_router(auth_backend)

# Router for user registration
register_router = fastapi_users.get_register_router(UserRead, UserCreate)

# Router for password reset
reset_password_router = fastapi_users.get_reset_password_router()

# 👇 NEW: Router for user self-service (get/update me) and admin management
# The /{id} routes are automatically protected to be superuser-only.
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

