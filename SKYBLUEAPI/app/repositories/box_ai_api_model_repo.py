from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.box_ai_api_model_model import BoxAiApiModel


class BoxAiApiModelRepository:
    async def get_all(self, db: AsyncSession, *, query: dict):
        page = query.get("page", 1)
        size = query.get("size", 50)

        statement = (
            select(
                BoxAiApiModel.id,
                BoxAiApiModel.name,
                BoxAiApiModel.name_en,
                BoxAiApiModel.description,
                BoxAiApiModel.logo_url,
                BoxAiApiModel.params,
                BoxAiApiModel.type,
            )
            .where(BoxAiApiModel.is_delete == 0)
            .order_by(BoxAiApiModel.id.desc())
        )

        total_statement = select(func.count()).select_from(statement.subquery())
        total = await db.scalar(total_statement) or 0

        result = await db.execute(statement.offset((page - 1) * size).limit(size))
        lists = [dict(row._mapping) for row in result.all()]

        return {
            "lists": lists,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size else 0,
        }


box_ai_api_model_repo = BoxAiApiModelRepository()
