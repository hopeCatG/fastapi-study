from app.repositories.user_repo import user_repo as repo
from app.schemas.user_schema import UserCreate, UserUpdate

# --- ASYNC VERSION ---
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    async def create(self, db: AsyncSession, *, payload: UserCreate):
        return await repo.create(db, obj_in=payload)

    async def get_by_id(self, db: AsyncSession, *, id: int):
        return await repo.get_by_id(db, id=id)
        
    # 👇 THIS METHOD IS NOW CORRECTED
    async def get_all(self, db: AsyncSession, *, query: dict):
        return await repo.get_all(db, query=query)

    async def update(self, db: AsyncSession, *, id: int, payload: UserUpdate):
        return await repo.update(db, id=id, obj_in=payload)

    async def delete(self, db: AsyncSession, *, id: int):
        return await repo.delete(db, id=id)

# This line is outside the conditional blocks
user_service = UserService()