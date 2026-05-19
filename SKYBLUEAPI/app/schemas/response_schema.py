from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    code: int = 200
    message: str = "success"
    data: T | None = None

class ListPage(BaseModel, Generic[T]):
    lists: list[T]
    total: int
    page: int
    size: int
    pages: int    

