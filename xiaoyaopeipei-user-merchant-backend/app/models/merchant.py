"""
商家模型
"""
from sqlalchemy import Column, BigInteger, String, Enum, DateTime
from app.models.base import BaseModel


class Merchant(BaseModel):
    """商家表"""

    __tablename__ = "merchants"

    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    shop_name = Column(String(100), nullable=False, comment="店铺名称")
    phone = Column(String(20), nullable=False, comment="联系电话")
    address = Column(String(255), nullable=True, comment="店铺地址")
    business_hours = Column(String(50), default="9:00-21:00", comment="营业时间")
    qrcode_url = Column(String(255), nullable=True, comment="二维码URL")
    shop_id = Column(String(100), unique=True, nullable=False, comment="店铺ID（如shop_123）")
    share_link = Column(String(500), unique=True, nullable=False, comment="完整分享链接")
    membership_expiry = Column(DateTime, nullable=True, comment="会员到期时间")
    status = Column(Enum("active", "inactive"), default="active", nullable=False, comment="状态")
