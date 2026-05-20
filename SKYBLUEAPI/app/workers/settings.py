import os

from dotenv import load_dotenv

load_dotenv()

try:
    from arq.connections import RedisSettings
except ModuleNotFoundError:
    print("\033[91m[ARQ ERROR] arq 未安装，无法启动 Worker。请执行 pip install arq\033[0m")
    raise SystemExit(1) from None

from app.workers.functions import poll_aigc_task

redis_settings = RedisSettings(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD") or None,
    database=int(os.getenv("REDIS_DB", "0")),
)


class WorkerSettings:
    functions = [poll_aigc_task]
    redis_settings = redis_settings
