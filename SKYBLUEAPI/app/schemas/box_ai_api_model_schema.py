from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BoxAiApiModelListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="主键ID")
    name: str | None = Field(default=None, description="名称")
    name_en: str | None = Field(default=None, description="英文名称")
    description: str | None = Field(default=None, description="描述")
    logo_url: str | None = Field(default=None, description="Logo 地址")
    params: Any | None = Field(default=None, description="参数")
    type: str | None = Field(default=None, description="类型")
