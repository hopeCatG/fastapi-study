from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.database import get_db

async def get_user_db(session: AsyncSession = Depends(get_db)):
    """
    Dependency that provides a user database adapter for FastAPI Users.
    This connects the user management logic to the SQLAlchemy session.
    """
    yield SQLAlchemyUserDatabase(session, User)
