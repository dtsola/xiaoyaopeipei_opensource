"""
统一异常处理中间件
捕获所有异常并返回统一格式的错误响应
"""
import time
import uuid
import traceback
from typing import Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logger import get_logger
from app.core.config import settings
from app.core.exceptions import AppException
from app.utils.response import error_response

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    应用异常处理器
    处理所有AppException及其子类异常
    """
    # 记录异常日志
    logger.error(f"AppException: {exc}", exc_info=True)

    # 如果是自定义AppException，直接使用其信息
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": exc.data,
                "timestamp": int(time.time() * 1000),
                "request_id": str(uuid.uuid4()),
            }
        )

    # 其他Exception按500处理
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误" if not settings.APP_DEBUG else str(exc),
            "data": traceback.format_exc() if settings.APP_DEBUG else None,
            "timestamp": int(time.time() * 1000),
            "request_id": str(uuid.uuid4()),
        }
    )


async def http_exception_handler(
    request: Request, exc: Union[StarletteHTTPException, Exception]
) -> JSONResponse:
    """
    HTTP异常处理器
    处理FastAPI/Starlette的HTTPException
    """
    # 记录异常日志
    logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}")

    # 获取状态码
    status_code = exc.status_code if hasattr(exc, "status_code") else 500

    # 获取详情
    detail = getattr(exc, "detail", "服务器错误")

    return JSONResponse(
        status_code=status_code,
        content={
            "code": status_code,
            "message": str(detail),
            "data": None,
            "timestamp": int(time.time() * 1000),
            "request_id": str(uuid.uuid4()),
        }
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    请求验证异常处理器
    处理Pydantic验证失败异常
    """
    # 记录异常日志
    logger.warning(f"Validation Error: {exc.errors()}")

    # 格式化验证错误信息
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "数据验证失败",
            "data": errors if settings.APP_DEBUG else None,
            "timestamp": int(time.time() * 1000),
            "request_id": str(uuid.uuid4()),
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    通用异常处理器
    捕获所有未被其他处理器处理的异常
    """
    # 记录异常日志
    logger.error(f"Unhandled Exception: {type(exc).__name__}: {exc}", exc_info=True)

    # 开发环境返回详细错误信息
    if settings.APP_DEBUG:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 500,
                "message": str(exc),
                "data": {
                    "type": type(exc).__name__,
                    "traceback": traceback.format_exc(),
                },
                "timestamp": int(time.time() * 1000),
                "request_id": str(uuid.uuid4()),
            }
        )

    # 生产环境返回通用错误信息
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误，请稍后重试",
            "data": None,
            "timestamp": int(time.time() * 1000),
            "request_id": str(uuid.uuid4()),
        }
    )
