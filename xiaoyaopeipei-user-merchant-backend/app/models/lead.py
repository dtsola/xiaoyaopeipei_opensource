"""
客户线索模型
"""
from sqlalchemy import Column, BigInteger, String, Enum, Text
from app.models.base import BaseModel


class Lead(BaseModel):
    """客户线索表"""

    __tablename__ = "leads"

    merchant_id = Column(BigInteger, nullable=False, comment="商家ID（软外键 → merchants.id）")
    conversation_id = Column(BigInteger, unique=True, nullable=False, comment="对话ID（软外键 → conversations.id）")
    phone = Column(String(255), nullable=False, comment="手机号（加密）")
    wechat = Column(String(255), nullable=True, comment="微信号（加密）")
    remark = Column(Text, nullable=True, comment="客户备注")
    budget = Column(String(50), nullable=True, comment="预算")
    device_type = Column(Enum("desktop", "laptop", "aio"), nullable=True, comment="设备类型")
    usage = Column(String(50), nullable=True, comment="用途")
    requirements = Column(Text, nullable=True, comment="具体需求")
    selected_sku_id = Column(BigInteger, nullable=True, comment="选中方案ID（软外键 → skus.id）")
    status = Column(
        Enum("pending", "contacted", "closed", "abandoned"),
        default="pending",
        nullable=False,
        comment="状态"
    )
    notes = Column(Text, nullable=True, comment="跟进记录数组（JSON）")
