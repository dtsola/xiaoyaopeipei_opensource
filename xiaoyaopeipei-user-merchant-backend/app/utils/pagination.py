"""
分页工具类
提供分页查询和响应格式化的工具函数
"""
import math
from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.base import PaginationSchema, PaginationParams

T = TypeVar("T")


def paginate_query(
    query: Any,
    params: PaginationParams,
) -> tuple:
    """
    对SQLAlchemy查询进行分页处理

    Args:
        query: SQLAlchemy查询对象
        params: 分页参数

    Returns:
        (分页后的查询, 总数)

    Example:
        query, total = paginate_query(select(Merchant), pagination_params)
        result = await session.execute(query.limit(params.limit).offset(params.skip))
        items = result.scalars().all()
    """
    # 计算总数（需要先执行count查询）
    count_query = select(func.count()).select_from(query.subquery())
    total = None  # 需要在调用处执行

    # 应用分页
    paginated_query = query.limit(params.limit).offset(params.skip)

    return paginated_query, total


async def get_paginated_result(
    session: AsyncSession,
    query: Any,
    params: PaginationParams,
) -> PaginationSchema:
    """
    执行分页查询并返回分页结果

    Args:
        session: 数据库会话
        query: SQLAlchemy查询对象
        params: 分页参数

    Returns:
        分页结果Schema
    """
    # 执行count查询获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar() or 0

    # 计算总页数
    pages = math.ceil(total / params.limit) if total > 0 else 0

    # 执行分页查询
    result = await session.execute(
        query.limit(params.limit).offset(params.skip)
    )
    items = result.scalars().all()

    # 转换为列表
    items_list = list(items)

    return PaginationSchema(
        items=items_list,
        total=total,
        page=params.page,
        limit=params.limit,
        pages=pages,
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    分页响应模型
    """
    code: int = 200
    message: str = "success"
    data: PaginationSchema
    timestamp: int
    request_id: Optional[str] = None


def create_paginated_response(
    items: List[T],
    total: int,
    page: int,
    limit: int,
    message: str = "success",
) -> dict:
    """
    创建分页响应

    Args:
        items: 数据列表
        total: 总数
        page: 当前页码
        limit: 每页数量
        message: 响应消息

    Returns:
        响应字典
    """
    import time
    import uuid

    pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "code": 200,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        },
        "timestamp": int(time.time() * 1000),
        "request_id": str(uuid.uuid4()),
    }
