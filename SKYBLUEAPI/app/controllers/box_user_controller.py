from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.routers import fastapi_users
from app.database import get_db
from app.models.box_user_model import BoxUser
from app.schemas.box_user_schema import BoxUserListItem
from app.schemas.response_schema import ApiResponse, ListPage
from app.services.box_user_service import box_user_service as service
from .dependencies import parse_query_params

current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/list", response_model=ApiResponse[ListPage[BoxUserListItem]], summary="获取用户列表（分页）")
async def get_box_users(
    query: dict = Depends(parse_query_params),
    db: AsyncSession = Depends(get_db),
    user: BoxUser = Depends(current_active_user), 
):
    """
    获取用户列表（分页）。

    仅返回字段：id、avatar、nickname、account、mobile、login_time。
    """
    data = await service.get_all(db, query=query)
    return JSONResponse(content=jsonable_encoder({"code": 200, "data": data, "message": "success"}))
