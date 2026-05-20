import asyncio
import json
import urllib.error
import os
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.routers import fastapi_users
from app.database import get_db
from app.models.ai_generated_images_model import AiGeneratedImages
from app.models.box_user_model import BoxUser
from app.schemas.aigc_schema import ToImageRequest
from app.utils.aigc_api import get_json, post_json
from app.utils.config import get_config_value
from app.utils.redis import get_arq_pool


current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(prefix="/aigc", tags=["aigc"])


@router.post("/to_image", summary="图片生成")
async def to_image(
    payload: ToImageRequest,
    db: AsyncSession = Depends(get_db),
    user: BoxUser = Depends(current_active_user),
):
    if not payload.prompt.strip():
        return JSONResponse(content={"code": 400, "data": None, "message": "提示词不能为空"})

    params = {
        "key": await get_config_value(db, "aigc_key") or "",
        "prompt": payload.prompt,
        "urls": payload.urls,
        "size": payload.size,
    }

    try:
        result = await asyncio.to_thread(
            post_json,
            f"{os.getenv('WUYINKEJI_API_URL', '')}/{payload.mode_type}",
            params,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return JSONResponse(content={"code": 500, "data": None, "message": f"请求失败: {exc}"})

    if result.get("code") != 200:
        return JSONResponse(content={"code": 400, "data": None, "message": result.get("msg", "请求失败")})

    result_data = result.get("data") or {}
    task_uuid = result_data.get("id")

    now = datetime.now()
    generate_type = "img2img" if params.get("urls") else "text2img"
    record = AiGeneratedImages(
        user_id=user.id,
        uuid=task_uuid,
        source="official",
        type=generate_type,
        category=payload.mode_type,
        prompt=params["prompt"],
        negative_prompt="",
        scale=params["size"],
        ratio="",
        points_cost=0,
        status=0,
        result_url="",
        parameter=json.dumps(params, ensure_ascii=False),
        is_delete=0,
        created_at=now,
        updated_at=now,
    )
    db.add(record)
    await db.commit()

    if task_uuid:
        arq_pool = await get_arq_pool()
        if arq_pool is None:
            return JSONResponse(
                content={
                    "code": 200,
                    "data": result_data,
                    "message": "任务创建成功，但 Redis 不可用，自动轮询未启用。请手动轮询 /aigc/task_status",
                }
            )
        try:
            await arq_pool.enqueue_job("poll_aigc_task", str(task_uuid), 1, _defer_by=5)
        except Exception as exc:
            return JSONResponse(
                content={
                    "code": 200,
                    "data": result_data,
                    "message": f"任务创建成功，但自动轮询入队失败。请手动轮询 /aigc/task_status。错误: {exc}",
                }
            )

    return JSONResponse(content=jsonable_encoder({"code": 200, "data": result_data, "message": "success"}))


@router.get("/task_status", summary="查询生成任务")
async def get_task_status(
    id: str = Query(default="", description="任务ID"),
    db: AsyncSession = Depends(get_db),
    user: BoxUser = Depends(current_active_user),
):
    task_id = id.strip()
    if not task_id:
        return JSONResponse(content={"code": 400, "data": None, "message": "任务ID不能为空"})

    params = {
        "key": await get_config_value(db, "aigc_key") or "",
        "id": task_id,
    }

    try:
        result = await asyncio.to_thread(
            get_json,
            f"{os.getenv('WUYINKEJI_API_URL', '')}/detail",
            params,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return JSONResponse(content={"code": 500, "data": None, "message": f"请求失败: {exc}"})

    if not result:
        return JSONResponse(content={"code": 400, "data": None, "message": "接口返回异常"})

    if result.get("code") != 200:
        return JSONResponse(content={"code": 400, "data": None, "message": result.get("msg", "查询失败")})

    result_data = result.get("data") or {}
    record_result = await db.execute(select(AiGeneratedImages).where(AiGeneratedImages.uuid == task_id))
    record = record_result.scalar_one_or_none()

    if record and int(record.status or 0) != 3 and result_data.get("status") == 2:
        urls = result_data.get("result") or []
        if isinstance(urls, list):
            urls = ",".join(str(url) for url in urls)
        elif not isinstance(urls, str):
            urls = ""

        if urls:
            record.result_url = urls
            record.status = 3
            record.updated_at = datetime.now()
            await db.commit()

    return JSONResponse(content=jsonable_encoder({"code": 200, "data": result_data, "message": "success"}))
