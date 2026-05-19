from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.models.box_user_model import BoxUser
from .backend import auth_backend
from .manager import get_user_manager

# FastAPIUsers instance: the core of the library
fastapi_users = FastAPIUsers[BoxUser, int](
    get_user_manager,
    [auth_backend],
)

# --- Routers ---

# Router for authentication (login, logout)
auth_router = fastapi_users.get_auth_router(auth_backend)

