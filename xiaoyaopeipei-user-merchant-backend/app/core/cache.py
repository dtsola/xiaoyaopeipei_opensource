"""
本地缓存管理（cachetools）
"""
from cachetools import TTLCache
from app.core.config import settings
from typing import Any, Optional


# 全局缓存实例
_cache: TTLCache = TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL)


def get_cache() -> TTLCache:
    """
    获取缓存实例

    Returns:
        TTLCache实例
    """
    return _cache


def cache_get(key: str) -> Optional[Any]:
    """
    从缓存获取数据

    Args:
        key: 缓存键

    Returns:
        缓存值，不存在返回None
    """
    return _cache.get(key)


def cache_set(key: str, value: Any, ttl: Optional[int] = None) -> None:
    """
    设置缓存数据

    Args:
        key: 缓存键
        value: 缓存值
        ttl: 过期时间（秒），默认使用配置值
    """
    if ttl:
        # 使用TTL设置临时缓存
        temp_cache = TTLCache(maxsize=1, ttl=ttl)
        temp_cache[key] = value
        _cache[key] = temp_cache[key]
    else:
        _cache[key] = value


def cache_delete(key: str) -> None:
    """
    删除缓存数据

    Args:
        key: 缓存键
    """
    if key in _cache:
        del _cache[key]


def cache_clear() -> None:
    """清空所有缓存"""
    _cache.clear()
