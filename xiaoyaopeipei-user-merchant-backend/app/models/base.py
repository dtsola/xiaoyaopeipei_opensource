"""
模型基类
"""
from sqlalchemy import Column, BigInteger, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base


class BaseModel(Base):
    """模型基类"""

    __abstract__ = True

    id = Column(BigInteger, primary_key=True, comment="主键（雪花算法）")
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    def to_dict(self):
        """转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
