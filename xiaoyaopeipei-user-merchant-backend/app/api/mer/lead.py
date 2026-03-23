"""
B端 - 线索管理接口
"""
import json
from typing import Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_merchant
from app.schemas.lead import LeadStatusUpdate, LeadNote, LeadListItem, LeadDetail
from app.models.merchant import Merchant
from app.models.sku import Sku
from app.schemas.base import PaginationParams
from app.utils.response import success_response
from app.core.logger import get_logger
from app.services.lead_service import lead_service
from app.services.sku_service import sku_service
from app.services.message_service import message_service
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.core.security import mask_phone, decrypt_data

router = APIRouter()
logger = get_logger(__name__)


@router.get("/leads")
async def get_lead_list(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="状态"),
    device_type: Optional[str] = Query(None, description="设备类型"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    pagination: PaginationParams = Depends(),
):
    """
    获取线索列表（分页）

    支持筛选：
    - status: 线索状态（pending/contacted/closed/abandoned）
    - device_type: 设备类型（desktop/laptop/aio）
    - start_date/end_date: 日期范围
    - search: 搜索关键词（备注、需求）
    """
    logger.info(
        f"获取线索列表: merchant_id={current_merchant.id}, "
        f"status={status}, device_type={device_type}"
    )

    # 计算分页偏移量
    skip = (pagination.page - 1) * pagination.limit

    # 查询线索列表
    leads, total = lead_service.get_by_merchant(
        db=db,
        merchant_id=current_merchant.id,
        skip=skip,
        limit=pagination.limit,
        status=status,
        device_type=device_type,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )

    # 转换为列表项格式
    items = []
    for lead in leads:
        # 获取选中的SKU信息
        selected_sku_info = None
        if lead.selected_sku_id:
            sku = sku_service.get_by_id(db, id=lead.selected_sku_id)
            if sku:
                selected_sku_info = {
                    "id": str(sku.id),  # 转换为字符串，避免前端精度丢失
                    "name": sku.name,
                    "price": float(sku.price),
                }

        items.append({
            "id": str(lead.id),  # 转换为字符串，避免前端精度丢失
            "phone": mask_phone(lead.phone),  # 脱敏手机号用于显示
            "phone_full": decrypt_data(lead.phone),  # 完整明文手机号用于复制
            "wechat": decrypt_data(lead.wechat) if lead.wechat else None,  # 解密微信号
            "budget": lead.budget,
            "device_type": lead.device_type,
            "usage": lead.usage,
            "requirements": lead.requirements,
            "selected_sku": selected_sku_info,
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        })

    # 计算总页数
    pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 0

    return success_response(
        data={
            "items": items,
            "total": total,
            "page": pagination.page,
            "limit": pagination.limit,
            "pages": pages,
        },
        message="success",
    )


@router.get("/leads/{lead_id}")
async def get_lead_detail(
    lead_id: str,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取线索详情

    包含完整信息（解密手机号、微信号、对话记录、跟进记录）
    """
    logger.info(f"获取线索详情: lead_id={lead_id}, merchant_id={current_merchant.id}")

    # 验证线索所有权
    if not lead_service.verify_ownership(
        db=db, lead_id=lead_id, merchant_id=current_merchant.id
    ):
        raise NotFoundException(message="线索不存在")

    # 获取线索详情
    detail = lead_service.get_lead_with_details(
        db=db, lead_id=lead_id, merchant_id=current_merchant.id
    )

    if not detail:
        raise NotFoundException(message="线索不存在")

    return success_response(
        data=detail,
        message="success",
    )


@router.put("/leads/{lead_id}/status")
async def update_lead_status(
    lead_id: str,
    status_data: LeadStatusUpdate,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    修改线索状态

    状态流转：
    - pending → contacted → closed
    - pending → contacted → abandoned
    - 任意状态 → abandoned
    """
    logger.info(
        f"修改线索状态: lead_id={lead_id}, status={status_data.status}, "
        f"merchant_id={current_merchant.id}"
    )

    # 验证状态值
    valid_statuses = ["pending", "contacted", "closed", "abandoned"]
    if status_data.status not in valid_statuses:
        raise BadRequestException(
            message=f"无效的状态值，可选值：{', '.join(valid_statuses)}"
        )

    # 获取线索
    lead = lead_service.get_by_id(db, id=lead_id)
    if not lead or lead.merchant_id != current_merchant.id:
        raise NotFoundException(message="线索不存在")

    # 更新状态
    lead = lead_service.update_status(db=db, lead=lead, status=status_data.status)

    logger.info(f"线索状态已更新: lead_id={lead_id}, new_status={lead.status}")

    return success_response(
        data={
            "id": lead.id,
            "status": lead.status,
            "updated_at": lead.updated_at.isoformat() if lead.updated_at else None,
        },
        message="状态修改成功",
    )


@router.post("/leads/{lead_id}/notes")
async def add_lead_note(
    lead_id: str,
    note_data: LeadNote,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    添加跟进备注

    每条备注包含：
    - content: 备注内容
    - created_by: 创建商家ID
    - created_at: 创建时间
    """
    logger.info(
        f"添加跟进备注: lead_id={lead_id}, merchant_id={current_merchant.id}, "
        f"content={note_data.content[:50]}..."
    )

    # 获取线索
    lead = lead_service.get_by_id(db, id=lead_id)
    if not lead or lead.merchant_id != current_merchant.id:
        raise NotFoundException(message="线索不存在")

    # 添加跟进记录
    lead = lead_service.add_note(
        db=db,
        lead=lead,
        content=note_data.content,
        merchant_id=current_merchant.id,
    )

    # 解析并返回最新的跟进记录列表
    try:
        notes = json.loads(lead.notes) if lead.notes else []
    except:
        notes = []

    return success_response(
        data={
            "id": str(lead.id),  # 转换为字符串，避免前端精度丢失
            "notes": notes,
            "updated_at": lead.updated_at.isoformat() if lead.updated_at else None,
        },
        message="备注添加成功",
    )


@router.get("/leads/{lead_id}/notes")
async def get_lead_notes(
    lead_id: str,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取线索的跟进记录列表
    """
    logger.info(f"获取跟进记录: lead_id={lead_id}, merchant_id={current_merchant.id}")

    # 获取线索
    lead = lead_service.get_by_id(db, id=lead_id)
    if not lead or lead.merchant_id != current_merchant.id:
        raise NotFoundException(message="线索不存在")

    # 解析跟进记录
    try:
        notes = json.loads(lead.notes) if lead.notes else []
    except:
        notes = []

    return success_response(
        data={
            "lead_id": lead.id,
            "notes": notes,
        },
        message="success",
    )


@router.get("/leads/stats/summary")
async def get_leads_stats_summary(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取线索统计摘要

    返回：
    - total: 总线索数
    - pending: 待处理线索数
    - contacted: 已联系线索数
    - closed: 已成交线索数
    - abandoned: 已放弃线索数
    - today_count: 今日新增线索数
    """
    logger.info(f"获取线索统计: merchant_id={current_merchant.id}")

    # 获取各状态线索数量
    from sqlalchemy import func
    from app.models.lead import Lead
    from datetime import date, timedelta

    # 各状态统计
    stats = {}
    for status in ["pending", "contacted", "closed", "abandoned"]:
        count = (
            db.query(func.count(Lead.id))
            .filter(
                Lead.merchant_id == current_merchant.id,
                Lead.status == status,
            )
            .scalar()
        )
        stats[status] = count or 0

    # 总线索数
    total = (
        db.query(func.count(Lead.id))
        .filter(Lead.merchant_id == current_merchant.id)
        .scalar()
    ) or 0

    # 今日新增
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_count = (
        db.query(func.count(Lead.id))
        .filter(
            Lead.merchant_id == current_merchant.id,
            Lead.created_at >= today_start,
        )
        .scalar()
    ) or 0

    return success_response(
        data={
            "total": total,
            "pending": stats.get("pending", 0),
            "contacted": stats.get("contacted", 0),
            "closed": stats.get("closed", 0),
            "abandoned": stats.get("abandoned", 0),
            "today_count": today_count,
        },
        message="success",
    )


@router.get("/leads/{lead_id}/messages")
async def get_lead_conversation_messages(
    lead_id: str,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取线索的对话消息列表

    返回该线索关联对话的完整消息记录
    """
    logger.info(f"获取线索对话消息: lead_id={lead_id}, merchant_id={current_merchant.id}")

    # 获取线索
    lead = lead_service.get_by_id(db, id=lead_id)
    if not lead or lead.merchant_id != current_merchant.id:
        raise NotFoundException(message="线索不存在")

    # 获取对话消息
    messages = message_service.get_by_conversation(
        db=db,
        conversation_id=lead.conversation_id,
        skip=0,
        limit=100,  # 最多返回100条消息
    )

    # 转换为前端格式
    items = []
    for msg in messages:
        items.append({
            "id": str(msg.id),
            "role": msg.role,  # "assistant" 或 "user"
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        })

    return success_response(
        data={
            "conversation_id": str(lead.conversation_id),
            "items": items,
            "total": len(items),
        },
        message="success",
    )
