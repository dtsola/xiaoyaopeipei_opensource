"""
商家Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MerchantBase(BaseModel):
    """商家基础Schema"""

    shop_name: str = Field(..., min_length=2, max_length=100, description="店铺名称")
    phone: str = Field(..., max_length=20, description="联系电话")
    address: Optional[str] = Field(None, max_length=255, description="店铺地址")
    business_hours: str = Field("9:00-21:00", max_length=50, description="营业时间")


class MerchantCreate(MerchantBase):
    """商家创建Schema"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=8, max_length=20, description="密码")


class MerchantUpdate(BaseModel):
    """商家更新Schema"""

    shop_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    business_hours: Optional[str] = Field(None, max_length=50)


class MerchantResponse(MerchantBase):
    """商家响应Schema"""

    id: str = Field(..., description="商家ID（字符串类型，避免前端精度丢失）")
    username: str = Field(..., description="用户名")
    qrcode_url: Optional[str] = Field(None, description="二维码URL")
    share_link: str = Field(..., description="分享链接")
    membership_expiry: Optional[datetime] = Field(None, description="会员到期时间")
    status: str = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class MerchantLogin(BaseModel):
    """商家登录Schema"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class MerchantAuthResponse(BaseModel):
    """商家认证响应Schema"""

    token: str = Field(..., description="JWT Token")
    user: MerchantResponse = Field(..., description="用户信息")
