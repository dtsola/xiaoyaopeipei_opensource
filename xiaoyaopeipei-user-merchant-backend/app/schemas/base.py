"""
基础Schema
"""
from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    """统一响应格式"""

    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")
    timestamp: int = Field(..., description="服务器时间戳（毫秒）")
    request_id: Optional[str] = Field(None, description="请求追踪ID")


class PaginationSchema(BaseModel):
    """分页格式"""

    items: list = Field(default_factory=list, description="数据列表")
    total: int = Field(0, description="总数")
    page: int = Field(1, description="当前页码")
    limit: int = Field(10, description="每页数量")
    pages: int = Field(0, description="总页数")


class PaginationParams(BaseModel):
    """分页请求参数"""

    page: int = Field(1, ge=1, description="页码")
    limit: int = Field(10, ge=1, le=100, description="每页数量")

    @property
    def skip(self) -> int:
        """计算跳过的记录数"""
        return (self.page - 1) * self.limit
