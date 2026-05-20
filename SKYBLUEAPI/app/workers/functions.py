import asyncio
from datetime import datetime

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.ai_generated_images_model import AiGeneratedImages
from app.utils.aigc_api import get_json
from app.utils.config import get_config_value

MAX_ATTEMPTS = 60
POLL_INTERVAL = 5


async def poll_aigc_task(ctx, task_uuid: str, attempt: int = 1):
    async with AsyncSessionLocal() as db:
        key = await get_config_value(db, "aigc_key") or ""

    params = {"key": key, "id": task_uuid}

    try:
        result = await asyncio.to_thread(
            get_json, "https://api.wuyinkeji.com/api/async/detail", params
        )
    except Exception:
        if attempt < MAX_ATTEMPTS:
            await ctx["redis"].enqueue_job(
                "poll_aigc_task", task_uuid, attempt + 1, _defer_by=POLL_INTERVAL
            )
        return {"done": False, "attempt": attempt}

    result_data = result.get("data") or {}

    if result_data.get("status") == 2:
        urls = result_data.get("result") or []
        if isinstance(urls, list):
            urls = ",".join(str(url) for url in urls)
        elif not isinstance(urls, str):
            urls = ""

        if urls:
            async with AsyncSessionLocal() as db:
                record_result = await db.execute(
                    select(AiGeneratedImages).where(AiGeneratedImages.uuid == task_uuid)
                )
                record = record_result.scalar_one_or_none()
                if record and int(record.status or 0) != 3:
                    record.result_url = urls
                    record.status = 3
                    record.updated_at = datetime.now()
                    await db.commit()

        return {"done": True, "uuid": task_uuid}

    if attempt < MAX_ATTEMPTS:
        await ctx["redis"].enqueue_job(
            "poll_aigc_task", task_uuid, attempt + 1, _defer_by=POLL_INTERVAL
        )

    return {"done": False, "attempt": attempt}
