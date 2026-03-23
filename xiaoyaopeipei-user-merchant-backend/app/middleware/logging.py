"""
日志中间件（Loguru）
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件
    """

    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()

        # 获取请求信息
        method = request.method
        url = request.url.path
        client_ip = request.client.host if request.client else "unknown"

        # 处理请求
        try:
            response = await call_next(request)
            status_code = response.status_code

            # 计算处理时间
            process_time = (time.time() - start_time) * 1000

            # 记录访问日志
            logger.bind(access=True).info(
                f"{client_ip} - {method} {url} - {status_code} - {process_time:.2f}ms"
            )

            # 添加响应头
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

            return response

        except Exception as e:
            # 计算处理时间
            process_time = (time.time() - start_time) * 1000

            # 记录错误日志
            logger.error(
                f"请求处理失败: {method} {url} - {client_ip} - {process_time:.2f}ms\n"
                f"错误: {str(e)}"
            )
            raise
