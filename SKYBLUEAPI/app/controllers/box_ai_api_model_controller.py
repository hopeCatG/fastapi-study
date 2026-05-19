from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.routers import fastapi_users
from app.database import get_db
from app.models.box_user_model import BoxUser
from app.schemas.box_ai_api_model_schema import BoxAiApiModelListItem
from app.schemas.response_schema import ApiResponse, ListPage
from app.services.box_ai_api_model_service import box_ai_api_model_service as service
from .dependencies import parse_query_params


current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(prefix="/model", tags=["model"])


@router.get(
    "/list",
    response_model=ApiResponse[ListPage[BoxAiApiModelListItem]],
    summary="获取 AI API 模型列表（分页）",
)
async def get_box_ai_api_models(
    query: dict = Depends(parse_query_params),
    db: AsyncSession = Depends(get_db),
    user: BoxUser = Depends(current_active_user),
):
    data = await service.get_all(db, query=query)
    return JSONResponse(content=jsonable_encoder({"code": 200, "data": data, "message": "success"}))
