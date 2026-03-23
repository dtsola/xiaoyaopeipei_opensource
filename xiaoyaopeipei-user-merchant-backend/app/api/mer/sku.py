"""
B端 - SKU管理接口
"""
import json
from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from sqlalchemy import and_, func

from app.api.deps import get_current_merchant, get_db
from app.schemas.sku import SkuCreate, SkuUpdate, SkuResponse, SkuListItem
from app.schemas.base import PaginationParams
from app.models.merchant import Merchant
from app.models.sku import Sku
from app.services.sku_service import sku_service
from app.core.exceptions import (
    SKUNotFoundException,
    ForbiddenException,
    BadRequestException,
)
from app.utils.response import success_response
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


# ==================== Schema定义 ====================

class BatchDeleteRequest(BaseModel):
    """批量删除请求"""
    ids: list[int] = Field(..., min_items=1, description="SKU ID列表")


# ==================== 接口实现 ====================

@router.get("/skus")
async def get_sku_list(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    device_type: Optional[str] = Query(None, description="设备类型（desktop/laptop/aio）"),
    status: Optional[str] = Query(None, description="状态（active/inactive）"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    pagination: PaginationParams = Depends(),
):
    """
    获取配置列表（分页）

    支持按设备类型、状态筛选，支持关键词搜索
    """
    logger.info(f"获取SKU列表: merchant_id={current_merchant.id}, device_type={device_type}, status={status}, search={search}")

    # 构建查询参数
    skip = pagination.skip
    limit = pagination.limit

    # 获取SKU列表和总数
    items, total = sku_service.get_by_merchant(
        db=db,
        merchant_id=current_merchant.id,
        skip=skip,
        limit=limit,
        device_type=device_type,
        status=status,
        search=search,
    )

    # 转换为列表项Schema
    items_list = [
        SkuListItem(
            id=str(item.id),  # 转换为字符串，避免前端精度丢失
            name=item.name,
            device_type=item.device_type,
            brand=item.brand,
            cpu=item.cpu,
            gpu=item.gpu,
            ram=item.ram,
            storage=item.storage,
            price=item.price,
            stock=item.stock,
            status=item.status,
            tags=json.loads(item.tags) if item.tags else None,
            images=json.loads(item.images) if item.images else None,
            view_count=item.view_count,
            select_count=item.select_count,
            created_at=item.created_at,
        )
        for item in items
    ]

    # 计算总页数
    import math
    pages = math.ceil(total / limit) if total > 0 else 0

    return success_response(
        data={
            "items": items_list,
            "total": total,
            "page": pagination.page,
            "limit": pagination.limit,
            "pages": pages,
        },
        message="success",
    )


@router.get("/skus/{sku_id}")
async def get_sku_detail(
    sku_id: str,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取配置详情

    获取指定SKU的详细信息，自动增加查看次数
    """
    logger.info(f"获取SKU详情: sku_id={sku_id}, merchant_id={current_merchant.id}")

    # 获取SKU
    sku = sku_service.get_by_id(db, id=sku_id)
    if not sku:
        raise SKUNotFoundException()

    # 验证归属
    if sku.merchant_id != current_merchant.id:
        raise ForbiddenException(message="无权访问此配置")

    # 增加查看次数
    sku = sku_service.increment_view_count(db=db, sku=sku)

    # 转换为响应Schema
    sku_response = SkuResponse(
        id=str(sku.id),  # 转换为字符串，避免前端精度丢失
        merchant_id=str(sku.merchant_id),  # 转换为字符串，避免前端精度丢失
        device_type=sku.device_type,
        name=sku.name,
        brand=sku.brand,
        model=sku.model,
        cpu=sku.cpu,
        gpu=sku.gpu,
        ram=sku.ram,
        storage=sku.storage,
        motherboard=sku.motherboard,
        power_supply=sku.power_supply,
        case=sku.case,
        screen=sku.screen,
        weight=sku.weight,
        battery=sku.battery,
        price=sku.price,
        stock=sku.stock,
        status=sku.status,
        tags=json.loads(sku.tags) if sku.tags else None,
        images=json.loads(sku.images) if sku.images else None,
        view_count=sku.view_count,
        select_count=sku.select_count,
        created_at=sku.created_at,
        updated_at=sku.updated_at,
    )

    return success_response(
        data=sku_response.dict(),
        message="success",
    )


@router.post("/skus")
async def create_sku(
    sku_data: SkuCreate,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    添加配置

    创建新的电脑配置
    """
    logger.info(f"创建SKU: merchant_id={current_merchant.id}, name={sku_data.name}")

    # 创建SKU
    sku = sku_service.create(
        db=db,
        merchant_id=current_merchant.id,
        sku_data=sku_data.dict(),
    )

    logger.info(f"SKU创建成功: id={sku.id}, name={sku.name}")

    return success_response(
        data={
            "id": str(sku.id),  # 转换为字符串，避免前端精度丢失
            "name": sku.name,
        },
        message="添加成功",
    )


@router.put("/skus/{sku_id}")
async def update_sku(
    sku_id: str,
    sku_data: SkuUpdate,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    编辑配置

    更新指定SKU的信息
    """
    logger.info(f"更新SKU: sku_id={sku_id}, merchant_id={current_merchant.id}")

    # 获取SKU
    sku = sku_service.get_by_id(db, id=sku_id)
    if not sku:
        raise SKUNotFoundException()

    # 验证归属
    if sku.merchant_id != current_merchant.id:
        raise ForbiddenException(message="无权修改此配置")

    # 过滤None值
    update_data = {k: v for k, v in sku_data.dict().items() if v is not None}

    if not update_data:
        raise BadRequestException(message="没有提供需要更新的字段")

    # 更新SKU
    sku = sku_service.update(
        db=db,
        sku=sku,
        update_data=update_data,
    )

    logger.info(f"SKU更新成功: id={sku.id}")

    return success_response(
        data={
            "id": str(sku.id),  # 转换为字符串，避免前端精度丢失
            "name": sku.name,
            "updated_at": sku.updated_at,
        },
        message="修改成功",
    )


@router.delete("/skus/{sku_id}")
async def delete_sku(
    sku_id: str,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    删除配置（物理删除）
    """
    logger.info(f"删除SKU: sku_id={sku_id}, merchant_id={current_merchant.id}")

    # 获取SKU
    sku = sku_service.get_by_id(db, id=sku_id)
    if not sku:
        raise SKUNotFoundException()

    # 验证归属
    if sku.merchant_id != current_merchant.id:
        raise ForbiddenException(message="无权删除此配置")

    # 删除SKU
    sku_service.delete(db=db, sku=sku)

    return success_response(
        data={"id": sku_id},
        message="删除成功",
    )


@router.delete("/skus")
async def batch_delete_skus(
    request_data: BatchDeleteRequest,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    批量删除配置

    批量软删除多个SKU
    """
    logger.info(f"批量删除SKU: merchant_id={current_merchant.id}, ids={request_data.ids}")

    # 批量删除
    success_count, failed_count = sku_service.batch_delete(
        db=db,
        merchant_id=current_merchant.id,
        sku_ids=request_data.ids,
    )

    logger.info(f"批量删除SKU完成: 成功={success_count}, 失败={failed_count}")

    return success_response(
        data={
            "success_count": success_count,
            "failed_count": failed_count,
        },
        message=f"批量删除成功，成功{success_count}个，失败{failed_count}个",
    )


@router.get("/skus/stats/summary")
async def get_sku_summary(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    获取SKU统计摘要

    返回当前商家的SKU数量统计
    """
    logger.info(f"获取SKU统计: merchant_id={current_merchant.id}")

    # 统计各类型SKU数量
    total = db.query(Sku).filter(Sku.merchant_id == current_merchant.id).count()
    active_count = db.query(Sku).filter(
        and_(
            Sku.merchant_id == current_merchant.id,
            Sku.status == "active"
        )
    ).count()
    inactive_count = db.query(Sku).filter(
        and_(
            Sku.merchant_id == current_merchant.id,
            Sku.status == "inactive"
        )
    ).count()

    # 按设备类型统计
    from sqlalchemy import case

    device_type_stats = db.query(
        Sku.device_type,
        func.count(Sku.id).label("count")
    ).filter(
        Sku.merchant_id == current_merchant.id
    ).group_by(Sku.device_type).all()

    device_stats = {
        item.device_type: item.count
        for item in device_type_stats
    }

    return success_response(
        data={
            "total": total,
            "active_count": active_count,
            "inactive_count": inactive_count,
            "device_type_stats": device_stats,
        },
        message="success",
    )
