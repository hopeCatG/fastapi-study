from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AiGeneratedImages(Base):
    __tablename__ = "box_ai_generated_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    uuid: Mapped[str | None] = mapped_column(String(255))
    source: Mapped[str | None] = mapped_column(String(50))
    type: Mapped[str | None] = mapped_column(String(50))
    category: Mapped[str | None] = mapped_column(String(50))
    prompt: Mapped[str | None] = mapped_column(Text)
    negative_prompt: Mapped[str | None] = mapped_column(Text)
    scale: Mapped[str | None] = mapped_column(String(15))
    ratio: Mapped[str | None] = mapped_column(String(255))
    points_cost: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[int] = mapped_column(Integer)
    result_url: Mapped[str | None] = mapped_column(Text)
    parameter: Mapped[str | None] = mapped_column(Text)
    is_delete: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime | None] = mapped_column(DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)
