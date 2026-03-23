"""Alembic环境配置"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 导入模型 - 确保所有模型都被导入，以便autogenerate能检测到
from app.db.base import Base
from app.models.merchant import Merchant
from app.models.sku import Sku
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.lead import Lead
from app.models.share_stat import ShareStat
from app.models.ai_log import AiLog

# 导入所有模型（用于autogenerate检测）
# 必须在target_metadata设置之前导入所有模型
__all__ = [Merchant, Sku, Conversation, Message, Lead, ShareStat, AiLog]

# 导入配置
from app.core.config import settings

# this is the Alembic Config object
config = context.config

# 设置数据库URL - 直接使用URL避免%字符被ConfigParser解析为插值语法
# 注意：不在config中设置URL，而是在run_migrations_*函数中直接使用

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # 直接使用settings.DATABASE_URL，避免ConfigParser的%插值问题
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # 直接创建引擎，避免ConfigParser的%插值问题
    from sqlalchemy import create_engine
    connectable = create_engine(settings.DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
