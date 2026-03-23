"""
SKU配置模型
"""
from sqlalchemy import Column, BigInteger, String, Enum, Integer, DECIMAL, Text
from app.models.base import BaseModel


class Sku(BaseModel):
    """配置表"""

    __tablename__ = "skus"

    merchant_id = Column(BigInteger, nullable=False, comment="商家ID（软外键 → merchants.id）")
    device_type = Column(
        Enum("desktop", "laptop", "aio"),
        nullable=False,
        comment="设备类型"
    )
    name = Column(String(100), nullable=False, comment="配置名称")
    brand = Column(String(50), nullable=False, comment="品牌")
    model = Column(String(100), nullable=True, comment="型号")
    cpu = Column(String(100), nullable=False, comment="处理器")
    gpu = Column(String(100), nullable=True, comment="显卡")
    ram = Column(String(50), nullable=False, comment="内存")
    storage = Column(String(50), nullable=False, comment="存储")
    motherboard = Column(String(100), nullable=True, comment="主板")
    power_supply = Column(String(100), nullable=True, comment="电源")
    case = Column(String(100), nullable=True, comment="机箱")
    screen = Column(String(100), nullable=True, comment="屏幕")
    weight = Column(String(20), nullable=True, comment="重量")
    battery = Column(String(50), nullable=True, comment="续航")
    price = Column(DECIMAL(10, 2), nullable=False, comment="价格")
    stock = Column(Integer, default=0, nullable=False, comment="库存")
    status = Column(Enum("active", "inactive"), default="active", nullable=False, comment="状态")
    tags = Column(Text, nullable=True, comment="标签数组（JSON）")
    images = Column(Text, nullable=True, comment="图片URL数组（JSON）")
    view_count = Column(Integer, default=0, nullable=False, comment="被查看次数")
    select_count = Column(Integer, default=0, nullable=False, comment="被选择次数")
