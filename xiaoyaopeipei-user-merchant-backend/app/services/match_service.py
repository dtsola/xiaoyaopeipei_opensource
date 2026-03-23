"""
SKU匹配服务 - 根据用户需求匹配最合适的配置
"""
from typing import List, Dict, Any, Optional
from decimal import Decimal
from sqlalchemy.orm import Session

from app.services.sku_service import sku_service
from app.models.sku import Sku
from app.core.logger import get_logger

logger = get_logger(__name__)


# ==================== 用途权重配置 ====================

USAGE_WEIGHTS = {
    "游戏": {
        "cpu": 0.25,
        "gpu": 0.35,
        "ram": 0.2,
        "storage": 0.1,
        "screen": 0.1,
    },
    "设计": {
        "cpu": 0.3,
        "gpu": 0.3,
        "ram": 0.25,
        "storage": 0.1,
        "screen": 0.05,
    },
    "编程": {
        "cpu": 0.35,
        "gpu": 0.15,
        "ram": 0.3,
        "storage": 0.15,
        "screen": 0.05,
    },
    "办公": {
        "cpu": 0.3,
        "gpu": 0.1,
        "ram": 0.25,
        "storage": 0.2,
        "screen": 0.15,
    },
    "学习": {
        "cpu": 0.25,
        "gpu": 0.15,
        "ram": 0.25,
        "storage": 0.2,
        "screen": 0.15,
    },
    "默认": {
        "cpu": 0.25,
        "gpu": 0.2,
        "ram": 0.25,
        "storage": 0.15,
        "screen": 0.15,
    },
}

# ==================== CPU性能评分 ====================

CPU_SCORES = {
    # Intel
    "i3": 30,
    "i5": 50,
    "i7": 70,
    "i9": 90,
    # AMD
    "R3": 30,
    "R5": 50,
    "R7": 70,
    "R9": 90,
    # Apple
    "M1": 55,
    "M2": 65,
    "M3": 75,
    "M1 Pro": 70,
    "M2 Pro": 80,
    "M3 Pro": 85,
}

# ==================== GPU性能评分 ====================

GPU_SCORES = {
    # NVIDIA
    "RTX 4090": 100,
    "RTX 4080": 95,
    "RTX 4070": 85,
    "RTX 4060": 75,
    "RTX 3060": 65,
    "GTX 1650": 40,
    # AMD
    "RX 7900": 95,
    "RX 7800": 85,
    "RX 7700": 75,
    "RX 7600": 65,
    # Apple
    "集成": 30,
}

# ==================== 内存容量评分 ====================

RAM_SCORES = {
    "8GB": 40,
    "16GB": 70,
    "32GB": 90,
    "64GB": 100,
}


# ==================== SKU匹配服务 ====================

class SKUMatchService:
    """SKU匹配服务"""

    def __init__(self):
        pass

    def _parse_budget(self, budget_str: str) -> tuple[Optional[int], Optional[int]]:
        """
        解析预算字符串

        Args:
            budget_str: 预算字符串，如"5000"、"5000-8000"

        Returns:
            (min_budget, max_budget)
        """
        try:
            budget_str = budget_str.replace("元", "").replace(" ", "").strip()

            if "-" in budget_str:
                parts = budget_str.split("-")
                min_budget = int(parts[0])
                max_budget = int(parts[1])
                return min_budget, max_budget
            else:
                budget = int(budget_str)
                # 允许±20%的浮动
                return int(budget * 0.8), int(budget * 1.2)
        except (ValueError, AttributeError):
            return None, None

    def _get_cpu_score(self, cpu_str: str) -> int:
        """获取CPU性能分数"""
        cpu_str = cpu_str.upper()
        for key, score in CPU_SCORES.items():
            if key.upper() in cpu_str:
                return score
        return 50  # 默认分数

    def _get_gpu_score(self, gpu_str: Optional[str]) -> int:
        """获取GPU性能分数"""
        if not gpu_str:
            return 30  # 集成显卡默认分数
        gpu_str = gpu_str.upper()
        for key, score in GPU_SCORES.items():
            if key.upper() in gpu_str:
                return score
        return 50  # 默认分数

    def _get_ram_score(self, ram_str: str) -> int:
        """获取内存容量分数"""
        ram_str = ram_str.upper().replace(" ", "")
        for key, score in RAM_SCORES.items():
            if key.replace(" ", "") in ram_str:
                return score
        # 尝试提取数字
        import re
        match = re.search(r"(\d+)GB?", ram_str)
        if match:
            size = int(match.group(1))
            if size <= 8:
                return 40
            elif size <= 16:
                return 70
            elif size <= 32:
                return 90
            else:
                return 100
        return 50

    def _calculate_budget_score(
        self, sku_price: Decimal, min_budget: int, max_budget: int
    ) -> float:
        """
        计算预算匹配分数

        Args:
            sku_price: SKU价格
            min_budget: 最低预算
            max_budget: 最高预算

        Returns:
            预算匹配分数（0-100）
        """
        price = float(sku_price)

        if min_budget is None or max_budget is None:
            return 50  # 没有预算限制，给中等分数

        if price < min_budget:
            # 低于预算，根据差距扣分
            diff_ratio = (min_budget - price) / min_budget
            return max(0, 100 - diff_ratio * 100)
        elif price > max_budget:
            # 超出预算，根据差距扣分
            diff_ratio = (price - max_budget) / max_budget
            return max(0, 100 - diff_ratio * 150)  # 超预算扣分更多
        else:
            # 在预算范围内
            budget_mid = (min_budget + max_budget) / 2
            diff_ratio = abs(price - budget_mid) / (max_budget - min_budget)
            return 100 - diff_ratio * 20

    def _calculate_spec_score(
        self,
        sku: Sku,
        usage: Optional[str] = None,
    ) -> float:
        """
        计算配置匹配分数

        Args:
            sku: SKU对象
            usage: 用途

        Returns:
            配置匹配分数（0-100）
        """
        # 获取用途权重
        weights = USAGE_WEIGHTS.get(usage, USAGE_WEIGHTS["默认"])

        # 计算各项分数
        cpu_score = self._get_cpu_score(sku.cpu)
        gpu_score = self._get_gpu_score(sku.gpu)
        ram_score = self._get_ram_score(sku.ram)
        storage_score = 70  # 存储暂给固定分数
        screen_score = 70  # 屏幕暂给固定分数

        # 加权计算
        total_score = (
            cpu_score * weights.get("cpu", 0.25)
            + gpu_score * weights.get("gpu", 0.2)
            + ram_score * weights.get("ram", 0.25)
            + storage_score * weights.get("storage", 0.15)
            + screen_score * weights.get("screen", 0.15)
        )

        return min(100, total_score)

    def _calculate_brand_preference(
        self,
        sku_brand: str,
        preferred_brand: Optional[str] = None,
    ) -> float:
        """
        计算品牌偏好匹配分数

        Args:
            sku_brand: SKU品牌
            preferred_brand: 用户偏好品牌

        Returns:
            品牌匹配分数（0-100）
        """
        if not preferred_brand:
            return 80  # 没有品牌偏好，给较高分数

        if preferred_brand.lower() in sku_brand.lower():
            return 100  # 品牌完全匹配
        else:
            return 60  # 品牌不匹配，降低分数

    def _parse_weight(self, weight_str: str) -> Optional[float]:
        """
        解析重量字符串

        Args:
            weight_str: 重量字符串，如"1.8kg"、"1.5kg"

        Returns:
            重量值（kg）
        """
        try:
            import re
            match = re.search(r"(\d+\.?\d*)\s*kg", weight_str.lower())
            if match:
                return float(match.group(1))
            return None
        except (AttributeError, ValueError):
            return None

    def _calculate_portable_bonus(
        self,
        sku: Sku,
        portable: Optional[str],
    ) -> float:
        """
        计算便携性加分

        Args:
            sku: SKU对象
            portable: 便携性需求

        Returns:
            加分（0-10）
        """
        if not portable:
            return 0

        portable_lower = portable.lower()
        bonus = 0

        # 1. 轻薄/便携需求
        if any(kw in portable_lower for kw in ["轻薄", "便携", "轻", "携带", "随身"]):
            # 台式机和一体机不符合便携需求，直接返回0分
            if sku.device_type in ["desktop", "aio"]:
                return 0

            weight = self._parse_weight(sku.weight) if sku.weight else None
            if weight:
                if weight < 1.5:
                    bonus += 10  # 非常轻
                elif weight < 2.0:
                    bonus += 7   # 比较轻
                elif weight < 2.5:
                    bonus += 4   # 还算轻
                elif weight < 3.0:
                    bonus += 2   # 稍重

        # 2. 续航需求
        if any(kw in portable_lower for kw in ["续航", "电池", "长续航"]):
            if sku.battery:
                # 有电池信息就加分（笔记本/一体机）
                bonus += 5
            elif sku.device_type == "desktop":
                # 台式机没有电池，不符合续航需求
                bonus = max(0, bonus - 5)

        return min(10, bonus)

    def calculate_match_score(
        self,
        sku: Sku,
        user_needs: Dict[str, Any],
    ) -> int:
        """
        计算SKU与用户需求的匹配分数

        Args:
            sku: SKU对象
            user_needs: 用户需求字典

        Returns:
            匹配分数（0-100）
        """
        scores = []

        # 1. 预算匹配（权重40%）
        budget = user_needs.get("budget")
        if budget:
            min_budget, max_budget = self._parse_budget(budget)
            budget_score = self._calculate_budget_score(
                sku.price, min_budget, max_budget
            )
            scores.append(("budget", budget_score, 0.4))

        # 2. 设备类型匹配（权重30%）
        device_type = user_needs.get("device_type")
        if device_type and sku.device_type:
            if device_type.lower() == sku.device_type.lower():
                scores.append(("device_type", 100, 0.3))
            else:
                scores.append(("device_type", 0, 0.3))

        # 3. 配置匹配（权重20%）
        usage = user_needs.get("usage")
        spec_score = self._calculate_spec_score(sku, usage)
        scores.append(("spec", spec_score, 0.2))

        # 4. 品牌偏好（权重10%）
        brand = user_needs.get("brand")
        brand_score = self._calculate_brand_preference(sku.brand, brand)
        scores.append(("brand", brand_score, 0.1))

        # 5. 便携性加分（不占权重，额外加分0-10分）
        portable = user_needs.get("portable")
        portable_bonus = self._calculate_portable_bonus(sku, portable)

        # 计算加权总分
        total_score = sum(score * weight for _, score, weight in scores) + portable_bonus

        # 格式化详情列表
        details = [(name, f"{s:.1f}", f"{w:.2f}") for name, s, w in scores]
        if portable_bonus > 0:
            details.append(("portable_bonus", f"+{portable_bonus:.1f}", "额外"))
        logger.debug(
            f"SKU[{sku.id}] {sku.name} 匹配分数: {total_score:.1f}, "
            f"详情: {details}"
        )

        return int(min(100, total_score))

    def match_skus(
        self,
        db: Session,
        merchant_id: int,
        user_needs: Dict[str, Any],
        top_n: int = 3,
    ) -> List[tuple[Sku, int]]:
        """
        匹配最合适的SKU

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            user_needs: 用户需求
            top_n: 返回前N个结果

        Returns:
            [(SKU, 匹配分数), ...] 按分数降序排列
        """
        # 获取商家的所有在售SKU
        skus, _ = sku_service.get_by_merchant(
            db=db,
            merchant_id=merchant_id,
            skip=0,
            limit=1000,  # 获取全部
            status="active",
        )

        if not skus:
            logger.warning(f"商家[{merchant_id}]没有在售的SKU")
            return []

        # 严格过滤：如果用户指定了设备类型，只匹配同类型的SKU
        user_device_type = user_needs.get("device_type")
        if user_device_type:
            skus = [sku for sku in skus if sku.device_type and sku.device_type.lower() == user_device_type.lower()]
            logger.info(f"设备类型过滤: {user_device_type}, 剩余SKU数: {len(skus)}")

        # 计算每个SKU的匹配分数
        results = []
        for sku in skus:
            score = self.calculate_match_score(sku, user_needs)
            # 只保留分数大于30的
            if score >= 30:
                results.append((sku, score))

        # 按分数降序排序
        results.sort(key=lambda x: x[1], reverse=True)

        # 返回前N个
        return results[:top_n]


# 创建全局实例
match_service = SKUMatchService()


def get_match_service() -> SKUMatchService:
    """
    获取SKU匹配服务实例

    Returns:
        SKU匹配服务单例
    """
    return match_service
