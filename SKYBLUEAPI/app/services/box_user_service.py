from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.box_user_repo import box_user_repo as repo


class BoxUserService:
    async def get_all(self, db: AsyncSession, *, query: dict):
        return await repo.get_all(db, query=query)


box_user_service = BoxUserService()

