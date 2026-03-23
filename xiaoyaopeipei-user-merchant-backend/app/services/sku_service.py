"""
SKU服务
"""
import json
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func

from app.models.sku import Sku
from app.models.merchant import Merchant
from app.utils.snowflake import generate_id


class SkuService:
    """SKU服务类"""

    def get_by_id(self, db: Session, id: int | str) -> Optional[Sku]:
        """根据ID获取SKU（支持字符串ID，自动转换为int）"""
        try:
            sku_id = int(id) if isinstance(id, str) else id
        except (ValueError, TypeError):
            return None
        return db.query(Sku).filter(Sku.id == sku_id).first()

    def get_by_merchant(
        self,
        db: Session,
        merchant_id: int,
        skip: int = 0,
        limit: int = 10,
        device_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Sku], int]:
        """
        获取商家的SKU列表（支持筛选和搜索）

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            skip: 跳过记录数
            limit: 返回记录数
            device_type: 设备类型筛选
            status: 状态筛选
            search: 搜索关键词

        Returns:
            (SKU列表, 总数)
        """
        # 构建查询
        query = db.query(Sku).filter(Sku.merchant_id == merchant_id)

        # 设备类型筛选
        if device_type:
            query = query.filter(Sku.device_type == device_type)

        # 状态筛选
        if status:
            query = query.filter(Sku.status == status)

        # 搜索关键词（名称、品牌、型号）
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Sku.name.like(search_pattern),
                    Sku.brand.like(search_pattern),
                    Sku.model.like(search_pattern),
                )
            )

        # 获取总数
        total = query.count()

        # 分页查询
        items = query.order_by(Sku.created_at.desc()).offset(skip).limit(limit).all()

        return items, total

    def create(
        self,
        db: Session,
        *,
        merchant_id: int,
        sku_data: dict,
    ) -> Sku:
        """
        创建SKU

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            sku_data: SKU数据

        Returns:
            创建的SKU对象
        """
        # 生成雪花ID
        sku_id = generate_id()

        # 处理JSON字段（空数组也要序列化）
        tags = json.dumps(sku_data.get("tags")) if sku_data.get("tags") is not None else None
        images = json.dumps(sku_data.get("images")) if sku_data.get("images") is not None else None

        sku = Sku(
            id=generate_id(),
            merchant_id=merchant_id,
            device_type=sku_data.get("device_type"),
            name=sku_data.get("name"),
            brand=sku_data.get("brand"),
            model=sku_data.get("model"),
            cpu=sku_data.get("cpu"),
            gpu=sku_data.get("gpu"),
            ram=sku_data.get("ram"),
            storage=sku_data.get("storage"),
            motherboard=sku_data.get("motherboard"),
            power_supply=sku_data.get("power_supply"),
            case=sku_data.get("case"),
            screen=sku_data.get("screen"),
            weight=sku_data.get("weight"),
            battery=sku_data.get("battery"),
            price=sku_data.get("price"),
            stock=sku_data.get("stock", 0),
            tags=tags,
            images=images,
        )

        db.add(sku)
        db.commit()
        db.refresh(sku)

        return sku

    def update(
        self,
        db: Session,
        *,
        sku: Sku,
        update_data: dict,
    ) -> Sku:
        """
        更新SKU

        Args:
            db: 数据库会话
            sku: SKU对象
            update_data: 更新数据

        Returns:
            更新后的SKU对象
        """
        # 更新字段
        for field, value in update_data.items():
            if value is not None and hasattr(sku, field):
                if field in ["tags", "images"]:
                    # JSON字段需要序列化
                    setattr(sku, field, json.dumps(value))
                else:
                    setattr(sku, field, value)

        db.commit()
        db.refresh(sku)

        return sku

    def delete(self, db: Session, *, sku: Sku) -> None:
        """
        删除SKU（物理删除）

        Args:
            db: 数据库会话
            sku: SKU对象

        Returns:
            None
        """
        db.delete(sku)
        db.commit()

    def batch_delete(
        self,
        db: Session,
        *,
        merchant_id: int,
        sku_ids: List[int],
    ) -> Tuple[int, int]:
        """
        批量删除SKU

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            sku_ids: SKU ID列表

        Returns:
            (成功数量, 失败数量)
        """
        success_count = 0
        failed_count = 0

        for sku_id in sku_ids:
            sku = self.get_by_id(db, id=sku_id)
            if sku and sku.merchant_id == merchant_id:
                self.delete(db=db, sku=sku)
                success_count += 1
            else:
                failed_count += 1

        return success_count, failed_count

    def increment_view_count(self, db: Session, *, sku: Sku) -> Sku:
        """
        增加查看次数

        Args:
            db: 数据库会话
            sku: SKU对象

        Returns:
            更新后的SKU对象
        """
        sku.view_count += 1
        db.commit()
        db.refresh(sku)
        return sku

    def increment_select_count(self, db: Session, *, sku: Sku) -> Sku:
        """
        增加选择次数

        Args:
            db: 数据库会话
            sku: SKU对象

        Returns:
            更新后的SKU对象
        """
        sku.select_count += 1
        db.commit()
        db.refresh(sku)
        return sku

    def verify_ownership(self, db: Session, *, sku_id: int, merchant_id: int) -> bool:
        """
        验证SKU是否属于指定商家

        Args:
            db: 数据库会话
            sku_id: SKU ID
            merchant_id: 商家ID

        Returns:
            是否属于该商家
        """
        sku = self.get_by_id(db, id=sku_id)
        return sku is not None and sku.merchant_id == merchant_id

    def get_available_brands(
        self,
        db: Session,
        merchant_id: int,
        limit: int = 10,
    ) -> List[str]:
        """
        获取商家的可用品牌列表（去重）

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            limit: 最多返回品牌数量

        Returns:
            品牌列表（按SKU数量降序）
        """
        # 查询该商家所有在售SKU的品牌，按数量排序
        results = (
            db.query(Sku.brand, func.count(Sku.id).label("count"))
            .filter(
                and_(
                    Sku.merchant_id == merchant_id,
                    Sku.status == "active",
                    Sku.brand.isnot(None),
                    Sku.brand != "",
                )
            )
            .group_by(Sku.brand)
            .order_by(func.count(Sku.id).desc())
            .limit(limit)
            .all()
        )

        # 返回品牌列表
        return [brand for brand, _ in results]

    def get_price_ranges(
        self,
        db: Session,
        merchant_id: int,
    ) -> List[str]:
        """
        根据店铺SKU价格分布，生成建议的预算区间

        Args:
            db: 数据库会话
            merchant_id: 商家ID

        Returns:
            预算区间列表，如 ["3000-5000元", "5000-8000元", ...]
        """
        # 获取该商家所有在售SKU的价格
        skus, _ = self.get_by_merchant(
            db=db,
            merchant_id=merchant_id,
            skip=0,
            limit=1000,
            status="active",
        )

        if not skus:
            # 没有SKU时返回默认区间
            return ["3000-5000元", "5000-8000元", "8000-12000元", "12000元以上"]

        # 提取价格
        prices = [float(sku.price) for sku in skus]
        min_price = min(prices)
        max_price = max(prices)

        # 根据价格范围生成合理的区间
        price_range = max_price - min_price

        if price_range < 500:
            # 价格区间很小或为0（所有SKU价格相同），以平均价格为中心生成浮动区间
            avg_price = (min_price + max_price) / 2
            # 使用1000元作为基准步长
            step = 1000
            ranges = [
                f"{int(avg_price - step)}-{int(avg_price)}元",
                f"{int(avg_price)}-{int(avg_price + step)}元",
                f"{int(avg_price + step)}-{int(avg_price + step * 2)}元",
                f"{int(avg_price + step * 2)}元以上",
            ]
        elif price_range < 2000:
            # 价格区间中等，生成中等区间
            step = (max_price - min_price) / 4
            ranges = []
            for i in range(4):
                start = int(min_price + i * step)
                end = int(min_price + (i + 1) * step)
                ranges.append(f"{start}-{end}元")
        elif price_range < 15000:
            # 价格区间较大，生成较宽区间
            ranges = [
                f"{int(min_price)}-{int(min_price + 3000)}元",
                f"{int(min_price + 3000)}-{int(min_price + 7000)}元",
                f"{int(min_price + 7000)}-{int(min_price + 12000)}元",
                f"{int(min_price + 12000)}元以上",
            ]
        else:
            # 价格区间很大，生成大区间
            ranges = [
                f"{int(min_price)}-{int(min_price + 5000)}元",
                f"{int(min_price + 5000)}-{int(min_price + 15000)}元",
                f"{int(min_price + 15000)}-{int(min_price + 30000)}元",
                f"{int(min_price + 30000)}元以上",
            ]

        return ranges


# 创建服务实例
sku_service = SkuService()
