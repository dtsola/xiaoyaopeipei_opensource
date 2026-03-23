"""
Loguru日志配置
"""
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

# 日志目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logger():
    """
    配置Loguru日志
    """
    # 移除默认的handler
    logger.remove()

    # 控制台输出（开发环境）
    if settings.APP_DEBUG:
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL,
            format=settings.LOG_FORMAT,
            colorize=True,
        )

    # 应用日志文件（INFO及以上）
    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        level="INFO",
        format=settings.LOG_FORMAT,
        rotation=settings.LOG_ROTATION,  # 每天00:00轮转
        retention=settings.LOG_RETENTION,  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8",
        enqueue=True,  # 异步写入
    )

    # 错误日志文件（ERROR及以上）
    logger.add(
        LOG_DIR / "error_{time:YYYY-MM-DD}.log",
        level="ERROR",
        format=settings.LOG_FORMAT,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        encoding="utf-8",
        enqueue=True,
        backtrace=True,  # 显示堆栈跟踪
        diagnose=True,  # 显示变量值
    )

    # 访问日志文件（单独记录API访问）
    logger.add(
        LOG_DIR / "access_{time:YYYY-MM-DD}.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        encoding="utf-8",
        enqueue=True,
        filter=lambda record: "access" in record["extra"],
    )

    logger.info("Loguru日志系统初始化成功")


def get_logger(name: str = __name__):
    """
    获取日志实例

    Args:
        name: 日志名称（通常使用 __name__）

    Returns:
        logger实例
    """
    return logger.bind(name=name)
