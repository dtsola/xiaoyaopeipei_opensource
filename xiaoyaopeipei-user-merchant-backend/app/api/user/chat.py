"""
C端 - 对话接口
"""
import json
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.api.deps import get_db
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    RecommendationRequest,
    RecommendationResponse,
    ExtractedInfo,
    RecommendationItem,
    SkuSpecs,
)
from app.utils.response import success_response
from app.core.logger import get_logger
from app.models.message import Message
from app.services.conversation_service import conversation_service
from app.services.message_service import message_service
from app.services.merchant_service import merchant_service
from app.services.sku_service import sku_service
from app.services.ai.intent_service import get_intent_service, ExtractedInfo as IntentInfo
from app.services.ai.recommend_service import get_recommend_reason_service
from app.services.ai.memory import get_conversation_memory, MemoryManager
from app.services.match_service import get_match_service
from app.services.share_stat_service import share_stat_service

router = APIRouter()
logger = get_logger(__name__)


# ==================== 辅助函数 ====================

def extracted_info_to_dict(info: ExtractedInfo) -> Dict[str, Any]:
    """将ExtractedInfo转换为字典"""
    return {
        "budget": info.budget,
        "device_type": info.device_type,
        "usage": info.usage,
        "requirements": info.requirements,
        "brand": info.brand,
        "portable": info.portable,
    }


def dict_to_extracted_info(data: Dict[str, Any]) -> ExtractedInfo:
    """将字典转换为ExtractedInfo"""
    return ExtractedInfo(
        budget=data.get("budget"),
        device_type=data.get("device_type"),
        usage=data.get("usage"),
        requirements=data.get("requirements"),
        brand=data.get("brand"),
        portable=data.get("portable"),
    )


def sku_to_recommendation_item(sku, match_score: int, ai_reason: str) -> RecommendationItem:
    """将SKU转换为RecommendationItem"""
    # 解析images字段
    images = []
    if sku.images:
        try:
            images = json.loads(sku.images)
        except:
            images = []

    return RecommendationItem(
        sku_id=str(sku.id),
        name=sku.name,
        device_type=sku.device_type,
        brand=sku.brand,
        price=float(sku.price),
        specs=SkuSpecs(
            cpu=sku.cpu,
            gpu=sku.gpu,
            ram=sku.ram,
            storage=sku.storage,
            screen=sku.screen,
            weight=sku.weight,
            battery=sku.battery,
        ),
        images=images,
        ai_reason=ai_reason,
        match_score=match_score,
    )


# ==================== 接口实现 ====================

@router.post("/chat/message")
async def send_message(
    request: ChatMessageRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    """
    发送消息（AI意图识别）

    核心流程（混合记忆方案）：
    1. 获取或创建对话
    2. 获取对话记忆（从缓存或数据库）
    3. 保存用户消息到数据库
    4. 添加用户消息到记忆
    5. 调用AI服务提取信息
    6. 生成AI回复
    7. 添加AI回复到记忆
    8. 保存AI消息到数据库
    9. 返回结果
    """
    logger.info(
        f"收到消息: session_id={request.session_id}, shop_id={request.shop_id}, "
        f"message={request.message[:50]}..."
    )

    # 1. 获取商家信息（通过shop_id）
    merchant = merchant_service.get_by_shop_id(db, shop_id=request.shop_id)
    if not merchant:
        from app.core.exceptions import NotFoundException
        raise NotFoundException(message="店铺不存在")

    merchant_id = merchant.id

    # 2. 获取或创建对话
    client_ip = http_request.client.host if http_request.client else None
    user_agent = http_request.headers.get("user-agent")

    conversation = conversation_service.get_or_create_by_session(
        db=db,
        merchant_id=merchant_id,
        session_id=request.session_id,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    # 3. 获取对话记忆（混合方案：内存缓存 + 数据库）
    memory = get_conversation_memory(
        conversation_id=conversation.id,
        db=db,
        max_messages=20,  # 最多保留20条消息在内存中（确保足够的历史上下文）
        max_tokens=3000,  # 最多3000 tokens
    )

    # 4. 检查是否是新对话（第一次咨询）
    is_first_message = len(memory) == 0

    # 5. 保存用户消息到数据库（持久化，用于商户端线索展示）
    user_message = message_service.create_user_message(
        db=db,
        conversation_id=conversation.id,
        content=request.message,
    )

    # 6. 添加用户消息到记忆
    memory.add_user_message(request.message)

    # 7. 从最后一条AI消息中获取之前收集的信息
    collected_info = {}
    if not is_first_message:
        # 从记忆中获取最后一条AI消息的 extracted_info
        last_assistant_msg = db.query(Message).filter(
            Message.conversation_id == conversation.id,
            Message.role == "assistant"
        ).order_by(Message.created_at.desc()).first()

        if last_assistant_msg and last_assistant_msg.extracted_info:
            try:
                collected_info = json.loads(last_assistant_msg.extracted_info)
            except:
                pass

    # 调试日志：检查收集的信息和历史
    logger.info(f"[DEBUG] chat.py collected_info: {collected_info}")
    logger.info(f"[DEBUG] chat.py history count: {len(memory.get_dict_messages())}")

    # 8. 获取店铺可用品牌列表（用于AI对话引导）
    available_brands = sku_service.get_available_brands(
        db=db,
        merchant_id=merchant_id,
        limit=20,
    )

    # 9. 调用意图识别服务（使用记忆中的历史消息）
    history = memory.get_dict_messages()
    intent_service = get_intent_service()
    response = intent_service.process_message(
        user_message=request.message,
        collected_info=collected_info,
        history=history,
        available_brands=available_brands,
    )

    # 10. 保存AI消息（合并之前累积的信息和本次新提取的信息）
    new_extracted_info = extracted_info_to_dict(response.extracted_info)

    # 调试日志：检查合并前后的数据
    logger.info(f"[DEBUG] chat.py collected_info (before merge): {collected_info}")
    logger.info(f"[DEBUG] chat.py new_extracted_info from AI: {new_extracted_info}")

    merged_info = {**collected_info}
    for key, value in new_extracted_info.items():
        if value is not None and value != "" and value != "null":
            merged_info[key] = value

    logger.info(f"[DEBUG] chat.py merged_info (after merge): {merged_info}")

    assistant_message = message_service.create_assistant_message(
        db=db,
        conversation_id=conversation.id,
        content=response.ai_response,
        extracted_info=merged_info,
        confidence=0.8,
    )

    # 11. 添加AI回复到记忆
    memory.add_assistant_message(response.ai_response)

    # 12. 如果是第一次咨询，记录统计
    if is_first_message:
        try:
            device_type = response.extracted_info.device_type or None
            budget = response.extracted_info.budget or None
            share_stat_service.increment_consult_count(
                db=db,
                merchant_id=merchant_id,
                device_type=device_type,
                budget=budget,
            )
            logger.info(f"记录咨询统计: merchant_id={merchant_id}, device_type={device_type}, budget={budget}")
        except Exception as e:
            logger.error(f"记录咨询统计失败: {e}")

    # 9. 更新对话状态（如果信息完整）
    if response.is_complete:
        conversation_service.update_status(
            db=db,
            conversation=conversation,
            status="completed",
        )

    # 10. 返回结果
    return success_response(
        data={
            "session_id": conversation.session_id,
            "ai_response": response.ai_response,
            "extracted_info": extracted_info_to_dict(response.extracted_info),
            "is_complete": response.is_complete,
            "next_action": response.next_action,
            "quick_replies": response.quick_replies,
        },
        message="success",
    )


@router.post("/chat/recommend")
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
):
    """
    获取推荐方案

    核心流程：
    1. 获取对话
    2. 验证商家
    3. 调用匹配服务获取SKU
    4. 生成AI推荐理由
    5. 返回推荐列表
    """
    logger.info(
        f"获取推荐: session_id={request.session_id}, shop_id={request.shop_id}, "
        f"needs={request.needs.model_dump()}"
    )

    # 1. 获取对话
    conversation = conversation_service.get_by_session_id(db, session_id=request.session_id)
    if not conversation:
        from app.core.exceptions import NotFoundException
        raise NotFoundException(message="对话不存在")

    # 2. 验证商家
    merchant = merchant_service.get_by_shop_id(db, shop_id=request.shop_id)
    if not merchant or merchant.id != conversation.merchant_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException(message="无权访问此店铺的推荐")

    # 3. 调用匹配服务
    match_service = get_match_service()
    user_needs = extracted_info_to_dict(request.needs)

    matched_skus = match_service.match_skus(
        db=db,
        merchant_id=merchant.id,
        user_needs=user_needs,
        top_n=3,
    )

    if not matched_skus:
        logger.warning(f"没有找到匹配的SKU: merchant_id={merchant.id}, needs={user_needs}")
        return success_response(
            data={
                "recommendations": [],
            },
            message="未找到匹配的配置方案",
        )

    # 4. 生成推荐理由
    recommendations = []
    for sku, score in matched_skus:
        # 生成简单的推荐理由
        reason = _generate_recommendation_reason(sku, request.needs, score)

        recommendations.append(
            sku_to_recommendation_item(sku, score, reason)
        )

    # 5. 增加SKU的选择次数
    for sku, _ in matched_skus:
        sku_service.increment_select_count(db=db, sku=sku)

    logger.info(
        f"推荐完成: session_id={request.session_id}, "
        f"推荐数量={len(recommendations)}"
    )

    return success_response(
        data={
            "recommendations": [r.model_dump() for r in recommendations],
        },
        message=f"为您找到{len(recommendations)}个推荐方案",
    )


def _generate_recommendation_reason(
    sku,
    needs: ExtractedInfo,
    score: int,
) -> str:
    """
    生成推荐理由（AI生成）

    Args:
        sku: SKU对象
        needs: 用户需求
        score: 匹配分数

    Returns:
        推荐理由文本
    """
    try:
        # 使用AI生成推荐理由
        reason_service = get_recommend_reason_service()
        return reason_service.generate_reason(
            sku=sku,
            user_needs=extracted_info_to_dict(needs),
            match_score=score,
        )
    except Exception as e:
        logger.error(f"AI生成推荐理由失败，使用降级方案: {e}")
        # 降级到简单模板
        return _fallback_reason_template(sku, needs, score)


def _fallback_reason_template(
    sku,
    needs: ExtractedInfo,
    score: int,
) -> str:
    """
    降级推荐理由模板（AI调用失败时使用）

    Args:
        sku: SKU对象
        needs: 用户需求
        score: 匹配分数

    Returns:
        推荐理由文本
    """
    reasons = []

    # 价格描述
    if needs.budget:
        reasons.append(f"价格{sku.price}元符合您的预算")

    # 用途描述
    if needs.usage:
        reasons.append(f"{sku.cpu}处理器{sku.ram}内存适合{needs.usage}使用")

    # 品牌描述
    if needs.brand and needs.brand.lower() in sku.brand.lower():
        reasons.append(f"选择了您偏好的{sku.brand}品牌")

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


@router.get("/chat/history")
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db),
):
    """
    获取对话历史

    Args:
        session_id: 会话ID

    Returns:
        对话历史消息列表
    """
    logger.info(f"获取对话历史: session_id={session_id}")

    # 获取对话
    conversation = conversation_service.get_by_session_id(db, session_id=session_id)
    if not conversation:
        from app.core.exceptions import NotFoundException
        raise NotFoundException(message="对话不存在")

    # 获取消息历史
    messages = message_service.get_by_conversation(
        db=db,
        conversation_id=conversation.id,
    )

    # 转换为响应格式
    history = []
    for msg in messages:
        history.append({
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        })

    return success_response(
        data={
            "session_id": session_id,
            "messages": history,
            "status": conversation.status,
        },
        message="success",
    )


# 导入Message模型（用于类型检查）
from app.models.message import Message
