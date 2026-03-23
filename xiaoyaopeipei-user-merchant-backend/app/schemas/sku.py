"""
SKU Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal


class SkuBase(BaseModel):
    """SKU基础Schema"""

    device_type: str = Field(..., description="设备类型（desktop/laptop/aio）")
    name: str = Field(..., min_length=2, max_length=100, description="配置名称")
    brand: str = Field(..., min_length=2, max_length=50, description="品牌")
    model: Optional[str] = Field(None, max_length=100, description="型号")
    cpu: str = Field(..., max_length=100, description="处理器")
    gpu: Optional[str] = Field(None, max_length=100, description="显卡")
    ram: str = Field(..., max_length=50, description="内存")
    storage: str = Field(..., max_length=50, description="存储")
    motherboard: Optional[str] = Field(None, max_length=100, description="主板")
    power_supply: Optional[str] = Field(None, max_length=100, description="电源")
    case: Optional[str] = Field(None, max_length=100, description="机箱")
    screen: Optional[str] = Field(None, max_length=100, description="屏幕")
    weight: Optional[str] = Field(None, max_length=20, description="重量")
    battery: Optional[str] = Field(None, max_length=50, description="续航")
    price: Decimal = Field(..., gt=0, description="价格")
    stock: int = Field(..., ge=0, description="库存")
    tags: Optional[List[str]] = Field(None, description="标签数组")
    images: Optional[List[str]] = Field(None, description="图片URL数组")


class SkuCreate(SkuBase):
    """SKU创建Schema"""

    pass


class SkuUpdate(BaseModel):
    """SKU更新Schema（所有字段可选）"""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, description="状态（active/inactive）")
    device_type: Optional[str] = Field(None, description="设备类型")
    brand: Optional[str] = Field(None, min_length=2, max_length=50)
    model: Optional[str] = Field(None, max_length=100)
    cpu: Optional[str] = Field(None, max_length=100)
    gpu: Optional[str] = Field(None, max_length=100)
    ram: Optional[str] = Field(None, max_length=50)
    storage: Optional[str] = Field(None, max_length=50)
    motherboard: Optional[str] = Field(None, max_length=100)
    power_supply: Optional[str] = Field(None, max_length=100)
    case: Optional[str] = Field(None, max_length=100)
    screen: Optional[str] = Field(None, max_length=100)
    weight: Optional[str] = Field(None, max_length=20)
    battery: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    images: Optional[List[str]] = None


class SkuResponse(SkuBase):
    """SKU响应Schema"""

    id: str = Field(..., description="配置ID（字符串类型，避免前端精度丢失）")
    merchant_id: str = Field(..., description="商家ID（字符串类型，避免前端精度丢失）")
    status: str = Field(..., description="状态")
    view_count: int = Field(..., description="被查看次数")
    select_count: int = Field(..., description="被选择次数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class SkuListItem(BaseModel):
    """SKU列表项Schema"""

    id: str = Field(..., description="配置ID（字符串类型，避免前端精度丢失）")
    name: str = Field(..., description="配置名称")
    device_type: str = Field(..., description="设备类型")
    brand: str = Field(..., description="品牌")
    cpu: str = Field(..., description="处理器")
    gpu: Optional[str] = Field(None, description="显卡")
    ram: str = Field(..., description="内存")
    storage: str = Field(..., description="存储")
    price: Decimal = Field(..., description="价格")
    stock: int = Field(..., description="库存")
    status: str = Field(..., description="状态")
    tags: Optional[List[str]] = Field(None, description="标签")
    images: Optional[List[str]] = Field(None, description="图片")
    view_count: int = Field(..., description="被查看次数")
    select_count: int = Field(..., description="被选择次数")
    created_at: datetime = Field(..., description="创建时间")
