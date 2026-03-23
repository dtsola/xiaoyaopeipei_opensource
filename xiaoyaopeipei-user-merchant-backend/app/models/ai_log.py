"""
AI调用日志模型
"""
from sqlalchemy import Column, BigInteger, String, Text, Integer, DECIMAL
from app.models.base import BaseModel


class AiLog(BaseModel):
    """AI调用日志表"""

    __tablename__ = "ai_logs"

    conversation_id = Column(BigInteger, nullable=False, comment="对话ID（软外键 → conversations.id）")
    api_type = Column(String(50), nullable=False, comment="API类型（extraction/recommendation/modify）")
    prompt = Column(Text, nullable=False, comment="Prompt内容")
    response = Column(Text, nullable=True, comment="AI响应")
    tokens = Column(Integer, nullable=True, comment="Token消耗")
    cost = Column(DECIMAL(10, 4), nullable=True, comment="成本（元）")
    response_time = Column(Integer, nullable=True, comment="响应时间（毫秒）")
    error_message = Column(Text, nullable=True, comment="错误信息")
    # created_at 由 BaseModel 提供
