"""
FastAPI应用入口
"""
import json
from datetime import datetime, date
from decimal import Decimal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import setup_logger, get_logger
from app.core.exceptions import AppException
from app.middleware.logging import LoggingMiddleware
from app.middleware.exception_handler import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

# API路由
from app.api.user import router as user_router
from app.api.mer import router as mer_router

# 初始化日志
logger = get_logger(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    """自定义JSON编码器，处理datetime等特殊类型"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class CustomJSONResponse(JSONResponse):
    """自定义JSONResponse，使用CustomJSONEncoder"""

    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CustomJSONEncoder,
        ).encode("utf-8")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    # 启动时执行
    setup_logger()
    logger.info("应用启动中...")
    logger.info(f"环境: {settings.APP_ENV}")
    logger.info(f"调试模式: {settings.APP_DEBUG}")

    yield

    # 关闭时执行
    logger.info("应用关闭")


def create_app() -> FastAPI:
    """
    创建FastAPI应用
    """
    # 根据环境决定CORS允许的域名
    cors_origins = settings.CORS_ORIGINS
    if settings.APP_ENV == "production":
        cors_origins = settings.CORS_ORIGINS_PROD
    elif settings.APP_DEBUG:
        cors_origins = ["*"]  # 开发环境允许所有域名

    app = FastAPI(
        title="小遥配配 API",
        description="AI对话式电脑导购助手",
        version="1.0.0",
        docs_url="/docs" if settings.APP_DEBUG else None,
        redoc_url="/redoc" if settings.APP_DEBUG else None,
        lifespan=lifespan,
        default_response_class=CustomJSONResponse,
    )

    # ==================== 异常处理器 ====================
    # 自定义应用异常
    app.add_exception_handler(AppException, app_exception_handler)
    # HTTP异常
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    # 验证异常
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # 通用异常
    app.add_exception_handler(Exception, general_exception_handler)

    # ==================== 中间件 ====================
    # CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # 日志中间件（Loguru）
    app.add_middleware(LoggingMiddleware)

    # ==================== 路由 ====================
    # C端路由
    app.include_router(user_router, prefix="/api/user")

    # B端路由
    app.include_router(mer_router, prefix="/api/mer")

    # ==================== 健康检查 ====================
    @app.get("/health", tags=["健康检查"])
    async def health_check():
        """健康检查接口"""
        return {"status": "ok", "env": settings.APP_ENV}

    logger.info("FastAPI应用创建成功")
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
    )
