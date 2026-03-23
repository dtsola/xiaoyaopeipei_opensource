"""
消息模型
"""
from sqlalchemy import Column, BigInteger, Enum, Text, DECIMAL
from app.models.base import BaseModel


class Message(BaseModel):
    """消息表"""

    __tablename__ = "messages"

    conversation_id = Column(BigInteger, nullable=False, comment="对话ID（软外键 → conversations.id）")
    role = Column(Enum("user", "assistant"), nullable=False, comment="角色")
    content = Column(Text, nullable=False, comment="消息内容")
    extracted_info = Column(Text, nullable=True, comment="AI提取的信息（JSON）")
    confidence = Column(DECIMAL(3, 2), nullable=True, comment="置信度")
