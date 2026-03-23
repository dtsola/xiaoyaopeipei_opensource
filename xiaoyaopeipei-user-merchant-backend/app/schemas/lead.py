"""
线索Schema
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class LeadSubmitRequest(BaseModel):
    """提交线索请求Schema"""

    session_id: str = Field(..., description="会话ID")
    shop_id: str = Field(..., description="店铺ID")
    sku_id: str = Field(..., description="选中的配置ID")
    phone: str = Field(..., pattern=r"^\d{11}$", description="手机号（11位数字）")
    wechat: Optional[str] = Field(None, max_length=50, description="微信号")
    remark: Optional[str] = Field(None, max_length=200, description="备注信息")


class ShopInfo(BaseModel):
    """店铺信息Schema"""

    shop_name: str = Field(..., description="店铺名称")
    phone: str = Field(..., description="店铺电话")
    address: str = Field(..., description="店铺地址")
    business_hours: str = Field(..., description="营业时间")


class LeadSubmitResponse(BaseModel):
    """提交线索响应Schema"""

    lead_id: str = Field(..., description="线索ID")
    shop_info: ShopInfo = Field(..., description="店铺信息")


class LeadNote(BaseModel):
    """跟进记录Schema"""

    content: str = Field(..., min_length=1, max_length=500, description="备注内容")


class LeadStatusUpdate(BaseModel):
    """线索状态更新Schema"""

    status: str = Field(..., description="状态（pending/contacted/closed/abandoned）")


class SelectedSkuInfo(BaseModel):
    """选中SKU信息Schema"""

    id: str = Field(..., description="配置ID（字符串类型，避免前端精度丢失）")
    name: str = Field(..., description="配置名称")
    price: float = Field(..., description="价格")


class LeadListItem(BaseModel):
    """线索列表项Schema"""

    id: str = Field(..., description="线索ID（字符串类型，避免前端精度丢失）")
    phone: str = Field(..., description="手机号（脱敏）")
    wechat: Optional[str] = Field(None, description="微信号")
    budget: Optional[str] = Field(None, description="预算")
    device_type: Optional[str] = Field(None, description="设备类型")
    usage: Optional[str] = Field(None, description="用途")
    requirements: Optional[str] = Field(None, description="具体需求")
    selected_sku: Optional[SelectedSkuInfo] = Field(None, description="选中方案")
    status: str = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")


class LeadDetail(BaseModel):
    """线索详情Schema"""

    id: str = Field(..., description="线索ID（字符串类型，避免前端精度丢失）")
    phone: str = Field(..., description="手机号")
    wechat: Optional[str] = Field(None, description="微信号")
    remark: Optional[str] = Field(None, description="客户备注")
    needs: Dict[str, Any] = Field(..., description="用户需求")
    conversation: Dict[str, Any] = Field(..., description="对话记录")
    selected_sku: Optional[SelectedSkuInfo] = Field(None, description="选中方案")
    notes: List[Dict[str, Any]] = Field(default_factory=list, description="跟进记录")
    status: str = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
