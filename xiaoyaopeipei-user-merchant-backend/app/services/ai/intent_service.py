"""
意图识别服务 - 信息收集核心逻辑
"""
from typing import Optional, Dict, Any, List
import json
from pydantic import BaseModel, Field

from app.services.ai.llm import get_llm_client
from app.services.ai.prompts.intent_prompts import INTENT_RECOGNITION_SYSTEM
from app.core.logger import get_logger

logger = get_logger(__name__)


# ==================== Schema定义 ====================

class ExtractedInfo(BaseModel):
    """收集的用户需求信息（6个字段）"""
    budget: Optional[str] = Field(None, description="预算")
    device_type: Optional[str] = Field(None, description="设备类型：desktop/laptop/aio")
    usage: Optional[str] = Field(None, description="用途：游戏/办公/设计/编程等")
    requirements: Optional[str] = Field(None, description="具体配置需求")
    brand: Optional[str] = Field(None, description="品牌偏好")
    portable: Optional[str] = Field(None, description="便携性需求")


class ChatResponse(BaseModel):
    """对话响应"""
    ai_response: str
    extracted_info: ExtractedInfo
    is_complete: bool = False
    next_action: str = "ask"  # ask: 继续收集 | recommend: 触发推荐
    quick_replies: List[str] = Field(default_factory=list)


# ==================== 工具函数 ====================

def _is_valid(v: Any) -> bool:
    """判断值是否有效（非空、非null）"""
    return v is not None and v != "" and v != "null"


def _filter_valid(data: Dict[str, Any]) -> Dict[str, Any]:
    """过滤有效值"""
    return {k: v for k, v in data.items() if _is_valid(v)}


def _format_info(data: Dict[str, Any]) -> str:
    """格式化信息为文本"""
    valid_data = _filter_valid(data)
    return "\n".join([f"- {k}: {v}" for k, v in valid_data.items()]) if valid_data else "暂无"


def _check_complete(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """检查信息完整性（3项必需）"""
    required = ["budget", "device_type", "usage"]
    missing = [f for f in required if not _is_valid(data.get(f))]
    return len(missing) == 0, missing


def _parse_json_response(text: str) -> Dict[str, Any]:
    """解析LLM返回的JSON"""
    clean = text.strip()
    if "```json" in clean:
        clean = clean.split("```json")[1].split("```")[0].strip()
    elif "```" in clean:
        clean = clean.split("```")[1].split("```")[0].strip()
    return json.loads(clean)


# ==================== 意图识别服务 ====================

class IntentRecognitionService:
    """信息收集服务"""

    # 必需字段
    REQUIRED_FIELDS = ["budget", "device_type", "usage"]

    def __init__(self):
        self.llm = get_llm_client()

    def extract_intent(self, user_message: str, collected_info: Dict[str, Any],
                       history: Optional[List] = None) -> Dict[str, Any]:
        """
        步骤1: 从用户消息中提取信息

        Args:
            user_message: 用户消息
            collected_info: 已收集的信息
            history: 对话历史

        Returns:
            新提取的信息
        """
        # 构建已收集信息提示
        collected_hint = ""
        if collected_info:
            valid = _filter_valid(collected_info)
            if valid:
                collected_hint = f"\n【已收集】\n" + "\n".join([f"- {k}: {v}" for k, v in valid.items()])
                collected_hint += "\n\n只提取新信息，已收集的返回null。"

        # 构建消息
        messages = [{"role": "system", "content": INTENT_RECOGNITION_SYSTEM + collected_hint}]
        if history:
            messages.extend(history[-10:])  # 最近10条历史
        messages.append({"role": "user", "content": user_message})

        # LLM提取
        result = self.llm.chat_with_structured_output(
            messages=messages,
            output_schema={
                "type": "object",
                "properties": {f: {"type": ["string", "null"]} for f in ExtractedInfo.model_fields},
            },
            temperature=0.3,
        )
        logger.info(f"提取结果: {result}")
        return result or {}

    def merge_info(self, collected_info: Dict[str, Any], new_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        步骤2: 合并信息（新值覆盖旧值）

        Args:
            collected_info: 已收集信息
            new_info: 新提取信息

        Returns:
            合并后的信息
        """
        merged = {**collected_info}
        for k, v in new_info.items():
            if _is_valid(v):
                merged[k] = v
        return merged

    def check_info_complete(self, info: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        步骤3: 检查信息完整性

        Args:
            info: 当前收集信息

        Returns:
            (是否完整, 缺失字段列表)
        """
        return _check_complete(info)

    def generate_chat_response(self, user_message: str, extracted: Dict[str, Any],
                               collected_info: Dict[str, Any], brands: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        步骤4: 生成对话回复

        Args:
            user_message: 用户消息
            extracted: 本次提取信息
            collected_info: 累计收集信息
            brands: 可用品牌列表

        Returns:
            {"ai_response": str, "quick_replies": List[str]}
        """
        # 计算状态
        merged = self.merge_info(collected_info, extracted)
        is_complete, missing = self.check_info_complete(merged)
        has_brand = _is_valid(merged.get("brand"))

        # 构建品牌提示
        brand_hint = ""
        if brands and not has_brand:
            all_brands = "、".join(brands)
            top_brands = "、".join(brands[:3])
            brand_hint = f"\n【可用品牌】{all_brands}\n首次推荐前3个：{top_brands}，追问时再展示其他。"

        # 构建缺失提示
        missing_hint = ""
        if missing:
            missing_map = {"budget": "预算", "device_type": "设备类型", "usage": "用途"}
            missing_cn = [missing_map.get(m, m) for m in missing]
            missing_hint = f"请补充：{'、'.join(missing_cn)}"

        # 设备类型映射（用于友好显示）
        device_type_map = {"desktop": "台式机", "laptop": "笔记本", "aio": "一体机"}

        # 构建已收集信息的复述模板（所有6个字段）
        summary_parts = []
        if _is_valid(merged.get("budget")):
            summary_parts.append(f"预算{merged.get('budget')}")
        if _is_valid(merged.get("device_type")):
            device_name = device_type_map.get(merged.get('device_type'), merged.get('device_type'))
            summary_parts.append(device_name)
        if _is_valid(merged.get("usage")):
            summary_parts.append(f"用于{merged.get('usage')}")
        if _is_valid(merged.get("requirements")):
            summary_parts.append(f"配置要求：{merged.get('requirements')}")
        if _is_valid(merged.get("brand")):
            summary_parts.append(f"偏好{merged.get('brand')}品牌")
        if _is_valid(merged.get("portable")):
            summary_parts.append(f"便携性：{merged.get('portable')}")

        summary_text = "、".join(summary_parts) if summary_parts else "您的需求"

        prompt = f"""你是AI导购助手，收集用户电脑需求。{brand_hint}

【已收集信息】
{_format_info(merged)}

【完整性状态】预算:{'✓' if _is_valid(merged.get('budget')) else '✗'} 设备:{'✓' if _is_valid(merged.get('device_type')) else '✗'} 用途:{'✓' if _is_valid(merged.get('usage')) else '✗'}
{f'【缺失项】{missing_hint}' if missing else ''}

用户说：{user_message}

【回复规则】
1. 信息完整时（三项都有✓）→ 复述："好的，{summary_text}。点击下方查看推荐。"
2. 信息不完整时（有✗项）→ 确认新信息，继续询问缺失项，绝对不能说"点击下方查看推荐"

【快捷回复规则】
- 信息完整时，快捷回复固定为：["查看推荐"]，不要添加任何其他选项
- 信息不完整时，快捷回复为缺失信息对应的选项
- 缺用途 → ["办公用途","游戏用途","设计用途","编程用途"]
- 缺设备 → ["台式机","笔记本","一体机"]
- 缺预算 → ["3000元以内","3000-5000元","5000-8000元","8000元以上"]

【重要】信息不完整时，ai_response中绝不能出现"查看推荐"、"为您推荐"等触发推荐的词语。

返回JSON：
```json
{{"ai_response": "回复内容", "quick_replies": ["选项"]}}
```"""

        try:
            response = self.llm.chat([{"role": "system", "content": prompt},
                                     {"role": "user", "content": "生成回复"}], temperature=0.7)
            result = _parse_json_response(response)
            if not result.get("ai_response"):
                logger.warning(f"无效响应: {result}")
                return {"ai_response": "好的，我明白了。", "quick_replies": []}
            return result
        except Exception as e:
            logger.error(f"生成回复失败: {e}")
            return {"ai_response": "抱歉，能再说一遍吗？", "quick_replies": []}

    def process_message(self, user_message: str, collected_info: Dict[str, Any],
                       history: Optional[List] = None, available_brands: Optional[List[str]] = None) -> ChatResponse:
        """
        主流程：处理用户消息

        Args:
            user_message: 用户消息
            collected_info: 已收集信息
            history: 对话历史
            available_brands: 可用品牌

        Returns:
            ChatResponse
        """
        try:
            # 1. 提取
            extracted = self.extract_intent(user_message, collected_info, history)
            logger.info(f"[DEBUG] extracted: {extracted}")

            # 2. 合并
            merged = self.merge_info(collected_info, extracted)
            logger.info(f"收集进度: collected_info={collected_info} + extracted={extracted} → merged={merged}")

            # 3. 检查完整性
            is_complete, missing = self.check_info_complete(merged)
            logger.info(f"[DEBUG] is_complete={is_complete}, missing={missing}")

            # 4. 生成回复
            response = self.generate_chat_response(user_message, extracted, merged, available_brands)

            # 5. 确定下一步动作
            next_action = "recommend" if is_complete else "ask"

            # 6. 处理快捷回复
            if is_complete:
                # 信息完整时，强制只显示"查看推荐"
                quick_replies = ["查看推荐"]
                if response.get("quick_replies") != ["查看推荐"]:
                    logger.debug(f"[DEBUG] 信息完整，强制覆盖快捷回复。原: {response.get('quick_replies', [])}")
            else:
                # 信息不完整时，移除"查看推荐"（防止AI误生成）
                quick_replies = response.get("quick_replies", [])
                if "查看推荐" in quick_replies:
                    quick_replies = [r for r in quick_replies if r != "查看推荐"]
                    logger.warning(f"[DEBUG] 信息不完整但AI返回了'查看推荐'，已移除。原: {response.get('quick_replies', [])}")

            return ChatResponse(
                ai_response=response.get("ai_response", "好的"),
                extracted_info=ExtractedInfo(**_filter_valid(merged)),
                is_complete=is_complete,
                next_action=next_action,
                quick_replies=quick_replies,
            )

        except Exception as e:
            logger.error(f"处理失败: {e}")
            return ChatResponse(
                ai_response="抱歉，能再说一遍吗？",
                extracted_info=ExtractedInfo(),
                is_complete=False,
                next_action="ask",
                quick_replies=[],
            )


# 全局实例
intent_service = IntentRecognitionService()


def get_intent_service() -> IntentRecognitionService:
    return intent_service