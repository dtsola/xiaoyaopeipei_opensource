"""
C端 - 店铺接口
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.merchant import Merchant
from app.utils.response import success_response
from app.core.logger import get_logger
from app.services.share_stat_service import share_stat_service
from app.services.sku_service import sku_service

router = APIRouter()
logger = get_logger(__name__)


@router.get("/shop/{shop_id}")
async def get_shop_info(
    shop_id: str,
    db: Session = Depends(get_db),
):
    """
    获取店铺信息

    Args:
        shop_id: 店铺ID（如shop_123），对应merchant表的shop_id字段
    """
    logger.info(f"获取店铺信息: shop_id={shop_id}")

    # 查询商家（通过shop_id字段）
    merchant = db.query(Merchant).filter(Merchant.shop_id == shop_id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="店铺不存在",
        )

    # 记录扫码统计
    try:
        share_stat_service.increment_scan_count(db, merchant.id)
    except Exception as e:
        logger.error(f"记录扫码统计失败: {e}")

    return success_response(
        data={
            "id": merchant.id,
            "shop_name": merchant.shop_name,
            "phone": merchant.phone,
            "address": merchant.address,
            "business_hours": merchant.business_hours,
            "qrcode_url": merchant.qrcode_url,
        },
        message="success",
    )


@router.get("/shop/{shop_id}/price-ranges")
async def get_price_ranges(
    shop_id: str,
    db: Session = Depends(get_db),
):
    """
    获取店铺建议的预算区间（根据SKU价格分布动态生成）

    Args:
        shop_id: 店铺ID
    """
    logger.info(f"获取店铺预算区间: shop_id={shop_id}")

    # 查询商家（通过shop_id字段）
    merchant = db.query(Merchant).filter(Merchant.shop_id == shop_id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="店铺不存在",
        )

    # 获取动态价格区间
    price_ranges = sku_service.get_price_ranges(db, merchant.id)

    return success_response(
        data={
            "price_ranges": price_ranges,
        },
        message="success",
    )
