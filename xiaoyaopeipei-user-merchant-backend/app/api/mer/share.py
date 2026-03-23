"""
B端 - 分享管理接口
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_merchant
from app.schemas.share import PosterRequest
from app.models.merchant import Merchant
from app.utils.response import success_response
from app.core.logger import get_logger
from app.utils.qrcode import get_qrcode_generator
from app.services.merchant_service import merchant_service
from app.services.share_stat_service import share_stat_service
from app.core.exceptions import BadRequestException

router = APIRouter()
logger = get_logger(__name__)


@router.get("/share/qrcode")
async def get_qrcode(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取专属二维码

    返回商家的专属二维码和分享链接
    - 如果已存在，直接返回
    - 如果不存在，自动生成并上传到OSS
    """
    logger.info(f"获取二维码: merchant_id={current_merchant.id}")

    # 使用二维码生成器（如果不存在则自动生成）
    qrcode_generator = get_qrcode_generator()

    # 检查是否需要生成新二维码
    qrcode_url = qrcode_generator.generate_shop_qrcode_if_not_exists(
        merchant_id=current_merchant.id,
        share_link=current_merchant.share_link,
        current_qrcode_url=current_merchant.qrcode_url,
    )

    # 如果生成了新的二维码URL，更新商家信息
    if qrcode_url != current_merchant.qrcode_url:
        current_merchant.qrcode_url = qrcode_url
        db.commit()
        logger.info(f"二维码URL已更新: merchant_id={current_merchant.id}, url={qrcode_url}")

    return success_response(
        data={
            "qrcode_url": qrcode_url,
            "shop_id": current_merchant.shop_id,
            "share_link": current_merchant.share_link,  # 完整URL
        },
        message="success",
    )


@router.post("/share/qrcode/refresh")
async def refresh_qrcode(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    刷新二维码

    强制重新生成二维码（即使已存在）
    """
    logger.info(f"刷新二维码: merchant_id={current_merchant.id}")

    # 生成新二维码
    qrcode_generator = get_qrcode_generator()
    new_qrcode_url = qrcode_generator.generate_merchant_qrcode(
        merchant_id=current_merchant.id,
        share_link=current_merchant.share_link,
    )

    # 更新商家信息
    current_merchant.qrcode_url = new_qrcode_url
    db.commit()

    logger.info(f"二维码已刷新: merchant_id={current_merchant.id}, url={new_qrcode_url}")

    return success_response(
        data={
            "qrcode_url": new_qrcode_url,
            "shop_id": current_merchant.shop_id,
            "share_link": current_merchant.share_link,
        },
        message="二维码已刷新",
    )


@router.post("/share/poster")
async def generate_poster(
    poster_data: PosterRequest,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    生成分享海报

    支持多种模板样式：
    - template_1: 简约风格
    - template_2: 商务风格
    - template_3: 活力风格

    注意：海报生成功能需要图片合成库，当前版本返回二维码URL
    """
    logger.info(f"生成海报: merchant_id={current_merchant.id}, template_id={poster_data.template_id}")

    # 验证模板ID
    valid_templates = ["template_1", "template_2", "template_3"]
    if poster_data.template_id not in valid_templates:
        raise BadRequestException(
            message=f"无效的模板ID，可选值：{', '.join(valid_templates)}"
        )

    # 当前版本：直接返回二维码URL
    # 完整版本需要使用Pillow进行图片合成
    qrcode_generator = get_qrcode_generator()
    qrcode_url = qrcode_generator.generate_shop_qrcode_if_not_exists(
        merchant_id=current_merchant.id,
        share_link=current_merchant.share_link,
        current_qrcode_url=current_merchant.qrcode_url,
    )

    # TODO: 实现海报合成功能
    # 1. 根据template_id选择背景图
    # 2. 添加商家名称、联系方式
    # 3. 合成二维码
    # 4. 上传到OSS

    return success_response(
        data={
            "poster_url": qrcode_url,  # 当前版本直接返回二维码
            "qrcode_url": qrcode_url,
        },
        message="海报生成成功",
    )


@router.get("/share/stats")
async def get_share_stats(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    period: str = Query("today", description="统计周期（today/week/month/all）"),
):
    """
    获取分享统计

    返回指定时间段的统计数据：
    - scan_count: 扫码数
    - consult_count: 咨询数
    - lead_count: 线索数
    - conversion_rate: 转化率（线索数/咨询数）
    - device_type_stats: 设备类型分布
    - budget_stats: 预算分布
    """
    logger.info(f"获取分享统计: merchant_id={current_merchant.id}, period={period}")

    # 验证period参数
    valid_periods = ["today", "week", "month", "all"]
    if period not in valid_periods:
        raise BadRequestException(
            message=f"无效的统计周期，可选值：{', '.join(valid_periods)}"
        )

    # 获取统计数据
    stats = share_stat_service.get_summary_stats(
        db=db,
        merchant_id=current_merchant.id,
        period=period,
    )

    return success_response(
        data=stats,
        message="success",
    )


@router.get("/share/stats/trend")
async def get_share_stats_trend(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    days: int = Query(7, description="统计天数", ge=1, le=30),
):
    """
    获取分享统计趋势

    返回最近N天的每日统计数据
    """
    logger.info(
        f"获取分享统计趋势: merchant_id={current_merchant.id}, days={days}"
    )

    # 获取趋势数据
    trend = share_stat_service.get_trend_stats(
        db=db,
        merchant_id=current_merchant.id,
        days=days,
    )

    return success_response(
        data={
            "trend": trend,
            "days": days,
        },
        message="success",
    )


@router.post("/share/stats/scan")
async def record_scan(
    shop_id: str = Query(..., description="店铺ID"),
    db: Session = Depends(get_db),
):
    """
    记录扫码行为（C端调用）

    当用户扫描商家二维码时调用此接口
    """
    logger.info(f"记录扫码: shop_id={shop_id}")

    # 获取商家信息
    merchant = merchant_service.get_by_shop_id(db, shop_id=shop_id)
    if not merchant:
        raise BadRequestException(message="店铺不存在")

    # 增加扫码数
    share_stat_service.increment_scan_count(db=db, merchant_id=merchant.id)

    return success_response(
        data={
            "shop_id": shop_id,
            "shop_name": merchant.shop_name,
        },
        message="扫码记录成功",
    )
