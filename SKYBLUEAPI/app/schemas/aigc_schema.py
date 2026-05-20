from pydantic import BaseModel, Field


class ToImageRequest(BaseModel):
    mode_type: str = Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_]+$", description="生成模式")
    prompt: str = Field(min_length=1, description="提示词")
    urls: str = Field(default="", description="参考图片地址")
    size: str = Field(default="", description="图片尺寸")
