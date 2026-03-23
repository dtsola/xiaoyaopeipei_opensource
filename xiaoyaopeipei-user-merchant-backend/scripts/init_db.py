"""
初始化数据库脚本
"""
from app.db.session import engine
from app.db.base import Base
from app.core.logger import get_logger

logger = get_logger(__name__)


def init_db():
    """
    初始化数据库（创建所有表）
    """
    logger.info("开始创建数据库表...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建成功")


if __name__ == "__main__":
    init_db()
