"""
分享统计模型
"""
from sqlalchemy import Column, BigInteger, Date, Integer, Text
from app.models.base import BaseModel


class ShareStat(BaseModel):
    """分享统计表"""

    __tablename__ = "share_stats"

    merchant_id = Column(BigInteger, nullable=False, comment="商家ID（软外键 → merchants.id）")
    date = Column(Date, nullable=False, comment="日期")
    scan_count = Column(Integer, default=0, nullable=False, comment="扫码数")
    consult_count = Column(Integer, default=0, nullable=False, comment="咨询数")
    lead_count = Column(Integer, default=0, nullable=False, comment="线索数")
    device_type_stats = Column(Text, nullable=True, comment="设备类型统计（JSON）")
    budget_stats = Column(Text, nullable=True, comment="预算分布统计（JSON）")
