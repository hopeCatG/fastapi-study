from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.box_config_model import BoxConfig


async def get_config_value(db: AsyncSession, name: str) -> str | None:
    statement = select(BoxConfig.value).where(BoxConfig.name == name).limit(1)
    return await db.scalar(statement)
