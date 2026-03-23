"""
对话模型
"""
from sqlalchemy import Column, BigInteger, String, Enum, Text
from app.models.base import BaseModel


class Conversation(BaseModel):
    """对话表"""

    __tablename__ = "conversations"

    merchant_id = Column(BigInteger, nullable=False, comment="商家ID（软外键 → merchants.id）")
    session_id = Column(String(50), unique=True, nullable=False, comment="会话ID")
    client_ip = Column(String(50), nullable=True, comment="客户IP")
    user_agent = Column(Text, nullable=True, comment="浏览器信息")
    source = Column(String(50), nullable=True, comment="来源（qrcode/link）")
    status = Column(
        Enum("active", "completed", "abandoned"),
        default="active",
        nullable=False,
        comment="状态"
    )
