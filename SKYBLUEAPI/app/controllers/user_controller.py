from fastapi import APIRouter, Depends
from fastapi_pagination import Page, add_pagination

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from .dependencies import parse_query_params

from app.auth.routers import fastapi_users
from app.models.user_model import User
from app.schemas.user_schema import UserRead
from app.services.user_service import user_service as service

# Dependency to get the current, active, superuser
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=Page[UserRead], summary="Get All Users (Admin Only)")
async def get_all_users(
    query: dict = Depends(parse_query_params),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_superuser)
):
    """
    (Admin Only) Retrieve a paginated and filterable list of all users.
    """
    return await service.get_all(db, query=query)

# Add pagination to the router
add_pagination(router)

