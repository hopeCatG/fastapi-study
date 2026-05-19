from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

from app.auth.routers import fastapi_users
from app.models.box_user_model import BoxUser
from app.schemas.box_user_schema import BoxUserInfo
from app.schemas.response_schema import ApiResponse
from app.services.user_service import user_service as service
from app.utils.cos import get_cos_url

# Dependency to get the current, active, superuser
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/info", response_model=ApiResponse[BoxUserInfo], summary="获取当前用户信息")
async def get_user_info(
    db: AsyncSession = Depends(get_db),
    user: BoxUser = Depends(current_active_user),
):
    data = await service.get_by_id(db, id=user.id)
    user_info = BoxUserInfo.model_validate(data).model_dump()
    user_info["avatar"] = get_cos_url(user_info.get("avatar"))
    return JSONResponse(content=jsonable_encoder({"code": 200, "data": user_info, "message": "success"}))
