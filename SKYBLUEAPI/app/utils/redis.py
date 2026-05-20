import os
import asyncio
import time
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_arq_pool: Any = None

_redis_config = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", "6379")),
    "password": os.getenv("REDIS_PASSWORD") or None,
    "database": int(os.getenv("REDIS_DB", "0")),
}

_connect_timeout = float(os.getenv("REDIS_CONNECT_TIMEOUT", "1.5"))
_retry_interval = float(os.getenv("REDIS_RETRY_INTERVAL", "30"))
_next_retry_at = 0.0

_arq_cache: dict[str, Any] = {}


def _print_error(msg: str):
    print(f"\033[91m[ARQ ERROR] {msg}\033[0m")


def _print_info(msg: str):
    print(f"\033[92m[ARQ INFO] {msg}\033[0m")


def _import_arq():
    if _arq_cache:
        return _arq_cache

    try:
        from arq.connections import ArqRedis, RedisSettings, create_pool
    except ModuleNotFoundError:
        _print_error("arq 未安装，自动轮询不可用。如需启用，请执行 pip install arq")
        _arq_cache["error"] = True
        return {}

    _redis_settings = RedisSettings(
        host=_redis_config["host"],
        port=_redis_config["port"],
        password=_redis_config["password"],
        database=_redis_config["database"],
    )
    _arq_cache["RedisSettings"] = RedisSettings
    _arq_cache["ArqRedis"] = ArqRedis
    _arq_cache["create_pool"] = create_pool
    _arq_cache["redis_settings"] = _redis_settings
    return _arq_cache


def _redis_target() -> str:
    return f'{_redis_config["host"]}:{_redis_config["port"]}/{_redis_config["database"]}'


async def _create_pool_with_timeout(arq: dict[str, Any]):
    return await asyncio.wait_for(
        arq["create_pool"](arq["redis_settings"]),
        timeout=_connect_timeout,
    )


async def create_arq_pool():
    arq = _import_arq()
    if not arq or "create_pool" not in arq:
        return None

    global _arq_pool
    try:
        _arq_pool = await _create_pool_with_timeout(arq)
        _print_info("Redis 连接池已就绪")
        return _arq_pool
    except Exception as exc:
        global _next_retry_at
        _next_retry_at = time.monotonic() + _retry_interval
        _print_error(f"无法连接 Redis({_redis_target()}): {exc}")
        _arq_pool = None
        return None


async def get_arq_pool():
    arq = _import_arq()
    if not arq or "create_pool" not in arq:
        return None

    global _arq_pool
    if _arq_pool is None:
        global _next_retry_at
        if time.monotonic() < _next_retry_at:
            return None
        try:
            _arq_pool = await _create_pool_with_timeout(arq)
            _print_info("Redis 连接池已就绪 (lazy)")
        except Exception as exc:
            _next_retry_at = time.monotonic() + _retry_interval
            _print_error(f"无法连接 Redis({_redis_target()}): {exc}")
            _arq_pool = None
    return _arq_pool


async def close_arq_pool():
    global _arq_pool
    if _arq_pool:
        try:
            await _arq_pool.close()
        except Exception:
            pass
        _arq_pool = None
