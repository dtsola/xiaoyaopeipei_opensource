"""
B端 - 首页看板接口（数据统计模块）
"""
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.api.deps import get_db, get_current_merchant
from app.models.merchant import Merchant
from app.models.lead import Lead
from app.models.share_stat import ShareStat
from app.models.sku import Sku
from app.utils.response import success_response
from app.core.logger import get_logger
from app.core.exceptions import BadRequestException
from app.services.share_stat_service import share_stat_service
from app.services.lead_service import lead_service

router = APIRouter()
logger = get_logger(__name__)


@router.get("/dashboard/summary")
async def get_merchant_summary(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取商家汇总统计数据

    返回：
    - 配置数量 (sku_count)
    - 客户线索总数 (lead_count)
    - 成交订单数 (closed_count)
    - 使用天数 (days_since_registration)
    """
    logger.info(f"获取商家汇总统计: merchant_id={current_merchant.id}")

    # 获取SKU数量
    sku_count = (
        db.query(func.count(Sku.id))
        .filter(
            Sku.merchant_id == current_merchant.id,
            Sku.status == "active",
        )
        .scalar()
    ) or 0

    # 获取线索总数
    lead_count = (
        db.query(func.count(Lead.id))
        .filter(Lead.merchant_id == current_merchant.id)
        .scalar()
    ) or 0

    # 获取成交订单数（closed状态的线索）
    closed_count = (
        db.query(func.count(Lead.id))
        .filter(
            Lead.merchant_id == current_merchant.id,
            Lead.status == "closed",
        )
        .scalar()
    ) or 0

    # 计算使用天数（从注册到现在）
    days_since_registration = 0
    if current_merchant.created_at:
        days_diff = (date.today() - current_merchant.created_at.date()).days
        days_since_registration = max(0, days_diff)

    return success_response(
        data={
            "sku_count": sku_count,
            "lead_count": lead_count,
            "closed_count": closed_count,
            "days_since_registration": days_since_registration,
        },
        message="success",
    )


@router.get("/dashboard")
async def get_dashboard(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取首页看板数据

    返回多维度统计数据：
    - 今日统计：扫码数、咨询数、线索数、转化率
    - 本周趋势：日期列表、线索数量列表
    - 最近线索：最近5条线索记录
    - 设备类型分布：desktop/laptop/aio占比
    - 预算分布：各价格区间的线索数量
    """
    logger.info(f"获取看板数据: merchant_id={current_merchant.id}")

    today = date.today()

    # 1. 今日统计
    today_stats = share_stat_service.get_summary_stats(
        db=db, merchant_id=current_merchant.id, period="today"
    )

    # 2. 本周趋势（最近7天）
    week_trend = share_stat_service.get_trend_stats(
        db=db, merchant_id=current_merchant.id, days=7
    )
    week_dates = [t["date"] for t in week_trend]
    week_lead_counts = [t["lead_count"] for t in week_trend]

    # 3. 最近线索（最近5条）
    recent_leads_query = (
        db.query(Lead)
        .filter(Lead.merchant_id == current_merchant.id)
        .order_by(desc(Lead.created_at))
        .limit(5)
        .all()
    )

    recent_leads = []
    for lead in recent_leads_query:
        recent_leads.append({
            "id": lead.id,
            "budget": lead.budget,
            "device_type": lead.device_type,
            "usage": lead.usage,
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        })

    # 4. 设备类型分布（最近30天）
    device_type_distribution = _get_device_type_distribution(
        db=db, merchant_id=current_merchant.id, days=30
    )

    # 5. 预算分布（最近30天）
    budget_distribution = _get_budget_distribution(
        db=db, merchant_id=current_merchant.id, days=30
    )

    return success_response(
        data={
            "today_stats": {
                "consult_count": today_stats.get("consult_count", 0),
                "lead_count": today_stats.get("lead_count", 0),
                "conversion_rate": today_stats.get("conversion_rate", 0),
                "consult_trend": today_stats.get("consult_trend", 0),
                "lead_trend": today_stats.get("lead_trend", 0),
                "conversion_trend": today_stats.get("conversion_trend", 0),
            },
            "week_stats": {
                "dates": week_dates,
                "lead_counts": week_lead_counts,
            },
            "recent_leads": recent_leads,
            "device_type_distribution": device_type_distribution,
            "budget_distribution": budget_distribution,
        },
        message="success",
    )


@router.get("/dashboard/trends")
async def get_dashboard_trends(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    days: int = Query(30, description="统计天数", ge=7, le=90),
):
    """
    获取趋势数据

    返回最近N天的详细趋势数据
    """
    logger.info(f"获取趋势数据: merchant_id={current_merchant.id}, days={days}")

    trend = share_stat_service.get_trend_stats(
        db=db, merchant_id=current_merchant.id, days=days
    )

    return success_response(
        data={
            "trend": trend,
            "days": days,
        },
        message="success",
    )


@router.get("/dashboard/conversion")
async def get_conversion_stats(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    period: str = Query("month", description="统计周期（week/month）"),
):
    """
    获取转化率统计

    计算漏斗转化：
    扫码数 → 咨询数 → 线索数
    返回各阶段的转化率
    """
    logger.info(
        f"获取转化率统计: merchant_id={current_merchant.id}, period={period}"
    )

    # 验证period参数
    valid_periods = ["week", "month"]
    if period not in valid_periods:
        raise BadRequestException(
            message=f"无效的统计周期，可选值：{', '.join(valid_periods)}"
        )

    # 获取统计数据
    stats = share_stat_service.get_summary_stats(
        db=db, merchant_id=current_merchant.id, period=period
    )

    # 计算转化率
    scan_to_consult = 0.0
    consult_to_lead = 0.0
    scan_to_lead = 0.0

    if stats["scan_count"] > 0:
        scan_to_consult = round(
            (stats["consult_count"] / stats["scan_count"]) * 100, 2
        )
        scan_to_lead = round((stats["lead_count"] / stats["scan_count"]) * 100, 2)

    if stats["consult_count"] > 0:
        consult_to_lead = round(
            (stats["lead_count"] / stats["consult_count"]) * 100, 2
        )

    return success_response(
        data={
            "scan_count": stats["scan_count"],
            "consult_count": stats["consult_count"],
            "lead_count": stats["lead_count"],
            "conversion_rates": {
                "scan_to_consult": scan_to_consult,  # 扫码→咨询
                "consult_to_lead": consult_to_lead,  # 咨询→线索
                "scan_to_lead": scan_to_lead,  # 扫码→线索（整体）
            },
        },
        message="success",
    )


@router.get("/dashboard/top-skus")
async def get_top_skus(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    limit: int = Query(10, description="返回数量", ge=5, le=50),
):
    """
    获取热门配置（Top N）

    按被选择次数排序，返回最热门的配置
    """
    logger.info(f"获取热门配置: merchant_id={current_merchant.id}, limit={limit}")

    # 查询SKU并按选择次数排序
    skus = (
        db.query(Sku)
        .filter(
            Sku.merchant_id == current_merchant.id,
            Sku.status == "active",
        )
        .order_by(desc(Sku.select_count))
        .limit(limit)
        .all()
    )

    # 解析images字段
    top_skus = []
    for sku in skus:
        images = []
        if sku.images:
            try:
                import json
                images = json.loads(sku.images)
            except:
                pass

        top_skus.append({
            "id": str(sku.id),  # 转换为字符串，避免前端精度丢失
            "name": sku.name,
            "device_type": sku.device_type,
            "brand": sku.brand,
            "price": float(sku.price),
            "select_count": sku.select_count,
            "view_count": sku.view_count,
            "images": images,
        })

    return success_response(
        data={
            "top_skus": top_skus,
            "total": len(top_skus),
        },
        message="success",
    )


@router.get("/dashboard/sku-stats")
async def get_sku_stats(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    sku_id: str = Query(..., description="SKU ID（字符串类型）"),
):
    """
    获取单个配置的统计数据

    返回指定SKU的查看次数、选择次数、转化率
    """
    logger.info(
        f"获取SKU统计: merchant_id={current_merchant.id}, sku_id={sku_id}"
    )

    # 将字符串ID转换为整数
    try:
        sku_id_int = int(sku_id)
    except ValueError:
        raise BadRequestException(message="无效的SKU ID")

    # 获取SKU
    sku = (
        db.query(Sku)
        .filter(
            Sku.id == sku_id_int,
            Sku.merchant_id == current_merchant.id,
        )
        .first()
    )

    if not sku:
        raise BadRequestException(message="配置不存在")

    # 计算转化率
    conversion_rate = 0.0
    if sku.view_count > 0:
        conversion_rate = round((sku.select_count / sku.view_count) * 100, 2)

    # 获取关联的线索数量
    lead_count = (
        db.query(func.count(Lead.id))
        .filter(
            Lead.merchant_id == current_merchant.id,
            Lead.selected_sku_id == sku_id_int,
        )
        .scalar()
    ) or 0

    return success_response(
        data={
            "sku_id": str(sku.id),  # 转换为字符串，避免前端精度丢失
            "sku_name": sku.name,
            "view_count": sku.view_count,
            "select_count": sku.select_count,
            "lead_count": lead_count,
            "conversion_rate": conversion_rate,
        },
        message="success",
    )


@router.get("/dashboard/performance")
async def get_performance_stats(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    period: str = Query("month", description="统计周期（week/month）"),
):
    """
    获取业绩统计

    返回商家整体业绩数据：
    - 总线索数
    - 各状态线索分布
    - 平均响应时间（暂不实现）
    - 成交线索数
    """
    logger.info(f"获取业绩统计: merchant_id={current_merchant.id}, period={period}")

    # 确定日期范围
    today = date.today()
    if period == "week":
        start_date = today - timedelta(days=7)
    else:  # month
        start_date = today - timedelta(days=30)

    # 查询线索总数
    total_leads = (
        db.query(func.count(Lead.id))
        .filter(
            Lead.merchant_id == current_merchant.id,
            Lead.created_at >= start_date,
        )
        .scalar()
    ) or 0

    # 各状态线索数量
    status_stats = {}
    for status in ["pending", "contacted", "closed", "abandoned"]:
        count = (
            db.query(func.count(Lead.id))
            .filter(
                Lead.merchant_id == current_merchant.id,
                Lead.status == status,
                Lead.created_at >= start_date,
            )
            .scalar()
        ) or 0
        status_stats[status] = count

    return success_response(
        data={
            "period": period,
            "total_leads": total_leads,
            "status_stats": status_stats,
            "closed_count": status_stats.get("closed", 0),
        },
        message="success",
    )


# ==================== 辅助函数 ====================

def _get_device_type_distribution(
    db: Session, merchant_id: int, days: int
) -> Dict[str, int]:
    """
    获取设备类型分布

    Args:
        db: 数据库会话
        merchant_id: 商家ID
        days: 统计天数

    Returns:
        设备类型分布字典
    """
    # 从share_stats中获取数据
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    stats = (
        db.query(ShareStat)
        .filter(
            ShareStat.merchant_id == merchant_id,
            ShareStat.date >= start_date,
            ShareStat.date <= end_date,
        )
        .all()
    )

    # 合并设备类型统计
    device_type_stats = {}
    for stat in stats:
        if stat.device_type_stats:
            try:
                import json
                stats_data = json.loads(stat.device_type_stats)
                for key, value in stats_data.items():
                    device_type_stats[key] = (
                        device_type_stats.get(key, 0) + value
                    )
            except:
                pass

    return device_type_stats


def _get_budget_distribution(
    db: Session, merchant_id: int, days: int
) -> Dict[str, int]:
    """
    获取预算分布

    Args:
        db: 数据库会话
        merchant_id: 商家ID
        days: 统计天数

    Returns:
        预算分布字典
    """
    # 从share_stats中获取数据
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    stats = (
        db.query(ShareStat)
        .filter(
            ShareStat.merchant_id == merchant_id,
            ShareStat.date >= start_date,
            ShareStat.date <= end_date,
        )
        .all()
    )

    # 合并预算统计
    budget_stats = {}
    for stat in stats:
        if stat.budget_stats:
            try:
                import json
                stats_data = json.loads(stat.budget_stats)
                for key, value in stats_data.items():
                    budget_stats[key] = budget_stats.get(key, 0) + value
            except:
                pass

    return budget_stats
