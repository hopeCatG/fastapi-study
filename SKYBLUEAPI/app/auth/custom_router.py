import hashlib
import inspect
import time
from decimal import Decimal

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.box_user_model import BoxUser
from .backend import cookie_transport, get_jwt_strategy

router = APIRouter()


class RegisterRequest(BaseModel):
    account: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=1, max_length=32)
    mobile: str = Field(min_length=1, max_length=32)
    nickname: str | None = Field(default=None, max_length=32)
    avatar: str | None = Field(default="resource/image/adminapi/default/default_avatar.png", max_length=200)
    sex: int = 1
    channel: int = 3


@router.put("/register", summary="注册")
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    account = payload.account.strip()
    mobile = payload.mobile.strip()
    nickname = (payload.nickname or account).strip()

    exists_statement = select(BoxUser).where((BoxUser.account == account) | (BoxUser.mobile == mobile))
    exists_result = await db.execute(exists_statement)
    exists_user = exists_result.scalar_one_or_none()
    if exists_user:
        if exists_user.account == account:
            return JSONResponse(status_code=200, content={"code": 400, "data": None, "message": "账号已存在"})
        return JSONResponse(status_code=200, content={"code": 400, "data": None, "message": "手机号已存在"})

    max_sn = await db.scalar(select(func.max(BoxUser.sn)))
    now = int(time.time())
    user = BoxUser(
        sn=(max_sn or 0) + 1,
        account=account,
        password=hashlib.md5(payload.password.encode("utf-8")).hexdigest(),
        mobile=mobile,
        nickname=nickname,
        avatar=payload.avatar or "",
        real_name="",
        sex=payload.sex,
        channel=payload.channel,
        is_admin=0,
        is_disable=0,
        login_ip="",
        login_time=0,
        invite=0,
        is_matchmaker=0,
        is_new_user=1,
        user_money=Decimal("0"),
        total_recharge_amount=Decimal("0"),
        total_commission=Decimal("0"),
        withdraw="",
        create_time=now,
        update_time=now,
        delete_time=0,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return JSONResponse(
        status_code=200,
        content={
            "code": 200,
            "data": {"id": user.id, "account": user.account, "mobile": user.mobile, "nickname": user.nickname},
            "message": "注册成功",
        },
    )


@router.post("/login", summary="登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    statement = select(BoxUser).where(BoxUser.account == form_data.username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        return JSONResponse(status_code=200, content={"code": 400, "data": None, "message": "账号不存在"})
    if not user.is_active:
        return JSONResponse(status_code=200, content={"code": 400, "data": None, "message": "账号已禁用"})

    # calculated = hashlib.md5(form_data.password.encode("utf-8")).hexdigest()
    # if calculated.lower() != (user.password or "").lower():
    #     return JSONResponse(status_code=400, content={"message": "密码错误"})

    strategy = get_jwt_strategy()
    token = strategy.write_token(user)
    if inspect.isawaitable(token):
        token = await token
    response = JSONResponse(
        status_code=200,
        content={"code": 200, "data": {"token": token, "token_type": "cookie", "user_id": user.id, "account": user.account}, "message": "登录成功"},
    )
    response.set_cookie(
        cookie_transport.cookie_name,
        token,
        max_age=cookie_transport.cookie_max_age,
        path=cookie_transport.cookie_path,
        domain=cookie_transport.cookie_domain,
        secure=cookie_transport.cookie_secure,
        httponly=cookie_transport.cookie_httponly,
        samesite=cookie_transport.cookie_samesite,
    )
    return response


@router.post("/logout", summary="退出登录")
async def logout():
    response = JSONResponse(status_code=200, content={"code": 200, "data": None, "message": "退出成功"})
    response.set_cookie(
        cookie_transport.cookie_name,
        "",
        max_age=0,
        path=cookie_transport.cookie_path,
        domain=cookie_transport.cookie_domain,
        secure=cookie_transport.cookie_secure,
        httponly=cookie_transport.cookie_httponly,
        samesite=cookie_transport.cookie_samesite,
    )
    return response
