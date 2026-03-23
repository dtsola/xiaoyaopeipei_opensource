"""
推荐理由生成服务 - 使用AI生成个性化推荐理由
"""
from typing import Dict, Any, Any as ModelType

from app.services.ai.llm import get_llm_client
from app.services.ai.prompts.intent_prompts import RECOMMEND_REASON_SYSTEM
from app.core.logger import get_logger

logger = get_logger(__name__)


class RecommendReasonService:
    """推荐理由生成服务"""

    def __init__(self):
        self.llm_client = get_llm_client()

    def generate_reason(
        self,
        sku: ModelType,
        user_needs: Dict[str, Any],
        match_score: int,
    ) -> str:
        """
        生成AI推荐理由

        Args:
            sku: SKU对象
            user_needs: 用户需求
            match_score: 匹配分数

        Returns:
            推荐理由文本
        """
        try:
            # 构建用户需求描述
            needs_desc = self._format_user_needs(user_needs)

            # 构建配置描述
            specs_desc = self._format_sku_specs(sku)

            # 使用prompt模板
            prompt = RECOMMEND_REASON_SYSTEM.format(
                user_needs=needs_desc,
                sku_name=sku.name,
                brand=sku.brand,
                price=float(sku.price),
                cpu=sku.cpu or "未配置",
                gpu=sku.gpu or "集成显卡",
                ram=sku.ram or "未配置",
                storage=sku.storage or "未配置",
                other_specs=specs_desc,
            )

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": "请生成推荐理由"}
            ]

            # 调用LLM
            response = self.llm_client.chat(
                messages=messages,
                temperature=0.7,  # 稍高温度，让理由更自然
            )

            result = response.strip()
            logger.info(f"生成推荐理由成功: sku_id={sku.id}, reason={result[:50]}...")
            return result

        except Exception as e:
            logger.error(f"生成推荐理由失败: {e}")
            # 降级到简单模板
            return self._fallback_reason(sku, user_needs, match_score)

    def _format_user_needs(self, needs: Dict[str, Any]) -> str:
        """格式化用户需求"""
        parts = []
        if needs.get("budget"):
            parts.append(f"预算{needs['budget']}元")
        if needs.get("device_type"):
            dt_map = {"desktop": "台式机", "laptop": "笔记本", "aio": "一体机"}
            device_name = dt_map.get(needs['device_type'], needs['device_type'])
            parts.append(f"设备类型{device_name}")
        if needs.get("usage"):
            parts.append(f"用途{needs['usage']}")
        if needs.get("brand"):
            parts.append(f"偏好{needs['brand']}品牌")
        if needs.get("requirements"):
            parts.append(f"具体要求：{needs['requirements']}")
        if needs.get("portable"):
            parts.append(f"便携性：{needs['portable']}")
        return "、".join(parts) if parts else "无特殊需求"

    def _format_sku_specs(self, sku) -> str:
        """格式化SKU其他配置"""
        parts = []
        if sku.screen:
            parts.append(f"屏幕{sku.screen}")
        if sku.weight:
            parts.append(f"重量{sku.weight}")
        if sku.battery:
            parts.append(f"电池{sku.battery}")
        return "、".join(parts) if parts else "无"

    def _fallback_reason(self, sku, needs: Dict[str, Any], score: int) -> str:
        """降级推荐理由"""
        reasons = []

        # 价格描述
        if needs.get("budget"):
            reasons.append(f"价格{sku.price}元符合您的预算")

        # 用途描述
        if needs.get("usage"):
            reasons.append(f"{sku.cpu}处理器{sku.ram}内存适合{needs['usage']}使用")

        # 品牌描述
        if needs.get("brand") and needs["brand"].lower() in sku.brand.lower():
            reasons.append(f"选择了您偏好的{sku.brand}品牌")

        # 具体需求描述
        if needs.get("requirements"):
            reasons.append(f"满足您提出的{needs['requirements']}要求")

        # 便携性描述
        if needs.get("portable"):
            if any(kw in needs['portable'] for kw in ["轻薄", "便携", "轻"]):
                if sku.weight:
                    reasons.append(f"重量{sku.weight}，符合您的便携需求")
            if "续航" in needs['portable'] and sku.battery:
                reasons.append(f"配备{sku.battery}电池，续航有保障")

        # 性能描述
        if sku.gpu:
            reasons.append(f"配备{sku.gpu}显卡，性能出色")

        # 匹配度描述
        if score >= 80:
            reasons.append(f"综合匹配度高达{score}分")

        # 组合理由
        if reasons:
            main_reason = reasons[0]
            if len(reasons) > 1:
                main_reason += "，" + "，".join(reasons[1:3])  # 最多再加2条
            return main_reason + "。"
        else:
            return f"{sku.brand} {sku.name}，{sku.cpu}/{sku.ram}/{sku.storage}，综合评分{score}分。"


# 创建全局实例
recommend_reason_service = RecommendReasonService()


def get_recommend_reason_service() -> RecommendReasonService:
    """
    获取推荐理由服务实例

    Returns:
        推荐理由服务单例
    """
    return recommend_reason_service