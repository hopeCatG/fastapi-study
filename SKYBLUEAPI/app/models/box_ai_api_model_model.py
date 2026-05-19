from typing import Any

from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BoxAiApiModel(Base):
    __tablename__ = "box_ai_api_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String(100))
    name_en: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    logo_url: Mapped[str | None] = mapped_column(String(255))
    params: Mapped[Any | None] = mapped_column(JSON)
    type: Mapped[str | None] = mapped_column(String(20))
    is_delete: Mapped[int] = mapped_column(Integer)
