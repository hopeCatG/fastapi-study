from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.box_ai_api_model_repo import box_ai_api_model_repo as repo


class BoxAiApiModelService:
    async def get_all(self, db: AsyncSession, *, query: dict):
        return await repo.get_all(db, query=query)


box_ai_api_model_service = BoxAiApiModelService()
