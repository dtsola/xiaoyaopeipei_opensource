"""
C端 - 线索接口
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.lead import LeadSubmitRequest, LeadSubmitResponse, ShopInfo
from app.utils.response import success_response
from app.core.logger import get_logger
from app.services.merchant_service import merchant_service
from app.services.conversation_service import conversation_service
from app.services.lead_service import lead_service
from app.services.message_service import message_service
from app.services.share_stat_service import share_stat_service
from app.core.exceptions import NotFoundException, BadRequestException
from app.models.message import Message

router = APIRouter()
logger = get_logger(__name__)


@router.post("/lead/submit")
async def submit_lead(
    request: LeadSubmitRequest,
    db: Session = Depends(get_db),
):
    """
    提交客户线索

    核心流程：
    1. 验证商家是否存在
    2. 验证对话是否存在且属于该商家
    3. 获取对话中提取的需求信息
    4. 创建线索（加密敏感信息）
    5. 更新对话状态为completed
    6. 返回线索ID和店铺信息
    """
    logger.info(
        f"提交线索: session_id={request.session_id}, shop_id={request.shop_id}, "
        f"phone={request.phone[:3]}****{request.phone[-4:]}, sku_id={request.sku_id}"
    )

    # 1. 验证商家是否存在（通过shop_id）
    merchant = merchant_service.get_by_shop_id(db, shop_id=request.shop_id)
    if not merchant:
        raise NotFoundException(message="店铺不存在")

    # 2. 验证对话是否存在且属于该商家
    conversation = conversation_service.get_by_session_id(
        db, session_id=request.session_id
    )
    if not conversation:
        raise NotFoundException(message="对话不存在")

    if conversation.merchant_id != merchant.id:
        raise BadRequestException(message="对话与店铺不匹配")

    # 3. 检查是否已提交过线索
    existing_lead = lead_service.get_by_conversation_id(db, conversation_id=conversation.id)
    if existing_lead:
        logger.info(f"对话已提交过线索: lead_id={existing_lead.id}")
        # 返回已有线索和店铺信息
        return success_response(
            data={
                "lead_id": str(existing_lead.id),
                "shop_info": {
                    "shop_name": merchant.shop_name,
                    "phone": merchant.phone,
                    "address": merchant.address or "",
                    "business_hours": merchant.business_hours,
                },
            },
            message="您已提交过线索",
        )

    # 4. 获取对话中AI提取的需求信息
    assistant_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id,
            Message.role == "assistant",
        )
        .order_by(Message.created_at.desc())
        .first()
    )

    budget = None
    device_type = None
    usage = None
    requirements = None

    if assistant_messages and assistant_messages.extracted_info:
        try:
            import json

            extracted = json.loads(assistant_messages.extracted_info)
            budget = extracted.get("budget")
            device_type = extracted.get("device_type")
            usage = extracted.get("usage")
            requirements = extracted.get("requirements")
        except:
            pass

    # 5. 创建线索
    try:
        sku_id = int(request.sku_id) if request.sku_id else None
    except ValueError:
        sku_id = None

    lead = lead_service.create(
        db=db,
        merchant_id=merchant.id,
        conversation_id=conversation.id,
        phone=request.phone,
        wechat=request.wechat,
        remark=request.remark,
        budget=budget,
        device_type=device_type,
        usage=usage,
        requirements=requirements,
        selected_sku_id=sku_id,
    )

    # 记录线索统计
    try:
        share_stat_service.increment_lead_count(db, merchant.id)
        logger.info(f"记录线索统计: merchant_id={merchant.id}")
    except Exception as e:
        logger.error(f"记录线索统计失败: {e}")

    # 6. 更新对话状态为completed
    conversation_service.update_status(db=db, conversation=conversation, status="completed")

    logger.info(f"线索创建成功: lead_id={lead.id}, conversation_id={conversation.id}")

    # 7. 返回结果
    return success_response(
        data={
            "lead_id": str(lead.id),
            "shop_info": {
                "shop_name": merchant.shop_name,
                "phone": merchant.phone,
                "address": merchant.address or "",
                "business_hours": merchant.business_hours,
            },
        },
        message="提交成功，商家会尽快联系您",
    )

