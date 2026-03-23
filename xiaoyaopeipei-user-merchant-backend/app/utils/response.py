"""
统一响应工具
"""
import time
import uuid
from typing import Optional, Any
from app.schemas.base import ResponseSchema


def success_response(data: Optional[Any] = None, message: str = "success") -> dict:
    """
    成功响应

    Args:
        data: 响应数据
        message: 响应消息

    Returns:
        响应字典
    """
    return ResponseSchema(
        code=200,
        message=message,
        data=data,
        timestamp=int(time.time() * 1000),
        request_id=str(uuid.uuid4()),
    ).dict()


def error_response(code: int, message: str, data: Optional[Any] = None) -> dict:
    """
    错误响应

    Args:
        code: 错误码
        message: 错误消息
        data: 响应数据

    Returns:
        响应字典
    """
    return ResponseSchema(
        code=code,
        message=message,
        data=data,
        timestamp=int(time.time() * 1000),
        request_id=str(uuid.uuid4()),
    ).dict()
