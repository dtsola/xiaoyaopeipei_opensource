"""
B端 - 认证接口
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.api.deps import get_current_merchant, get_current_merchant_optional_membership, get_db
from app.schemas.merchant import MerchantCreate, MerchantLogin, MerchantUpdate
from app.models.merchant import Merchant
from app.services.merchant_service import merchant_service
from app.core.security import create_access_token, verify_password
from app.core.exceptions import (
    MerchantExistsException,
    InvalidCredentialsException,
)
from app.utils.response import success_response
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


# ==================== Schema定义 ====================

class PasswordUpdateRequest(BaseModel):
    """密码更新请求"""
    old_password: str = Field(..., min_length=1, description="旧密码")
    new_password: str = Field(..., min_length=8, max_length=20, description="新密码")


class MembershipRenewalRequest(BaseModel):
    """会员续期请求"""
    days: int = Field(..., ge=1, le=365, description="续期天数")


# ==================== 接口实现 ====================

@router.post("/auth/register")
async def register(
    merchant_data: MerchantCreate,
    db: Session = Depends(get_db),
):
    """
    商家注册

    创建新商家账号，注册成功后自动登录
    """
    logger.info(f"商家注册请求: username={merchant_data.username}")

    # 检查用户名是否已存在
    existing_merchant = merchant_service.get_by_username(db, username=merchant_data.username)
    if existing_merchant:
        raise MerchantExistsException()

    # 创建商家
    merchant = merchant_service.create(
        db=db,
        username=merchant_data.username,
        password=merchant_data.password,
        shop_name=merchant_data.shop_name,
        phone=merchant_data.phone,
        address=merchant_data.address,
        business_hours=merchant_data.business_hours,
    )

    # 生成Token
    token = create_access_token(data={"sub": str(merchant.id)})

    logger.info(f"商家注册成功: id={merchant.id}, username={merchant.username}")

    return success_response(
        data={
            "token": token,
            "user": {
                "id": str(merchant.id),  # 转换为字符串，避免前端精度丢失
                "username": merchant.username,
                "shop_name": merchant.shop_name,
                "shop_id": merchant.shop_id,
                "share_link": merchant.share_link,
                "membership_expiry": merchant.membership_expiry,
            },
        },
        message="注册成功",
    )


@router.post("/auth/login")
async def login(
    credentials: MerchantLogin,
    db: Session = Depends(get_db),
):
    """
    商家登录

    使用用户名和密码登录，成功后返回JWT Token
    """
    logger.info(f"商家登录请求: username={credentials.username}")

    # 验证用户名和密码
    merchant = merchant_service.authenticate(
        db=db,
        username=credentials.username,
        password=credentials.password,
    )

    if not merchant:
        raise InvalidCredentialsException()

    # 生成Token
    token = create_access_token(data={"sub": str(merchant.id)})

    # 检查会员是否过期
    is_membership_expired = (
        merchant.membership_expiry and
        merchant.membership_expiry < datetime.now()
    )
    # 检查是否需要会员到期提醒
    show_expiry_warning = merchant_service.check_membership_expiry_warning(merchant)

    logger.info(f"商家登录成功: id={merchant.id}, username={merchant.username}")

    return success_response(
        data={
            "token": token,
            "user": {
                "id": str(merchant.id),  # 转换为字符串，避免前端精度丢失
                "username": merchant.username,
                "shop_name": merchant.shop_name,
                "phone": merchant.phone,
                "shop_id": merchant.shop_id,
                "share_link": merchant.share_link,
                "membership_expiry": merchant.membership_expiry,
                "is_membership_expired": is_membership_expired,
                "show_expiry_warning": show_expiry_warning,
            },
        },
        message="登录成功",
    )


@router.get("/auth/me")
async def get_current_user(
    current_merchant: Merchant = Depends(get_current_merchant_optional_membership),
    db: Session = Depends(get_db),
):
    """
    获取当前用户信息

    获取当前登录商家的详细信息
    """
    # 检查会员是否过期
    is_membership_expired = (
        current_merchant.membership_expiry and
        current_merchant.membership_expiry < datetime.now()
    )
    # 检查是否需要会员到期提醒
    show_expiry_warning = merchant_service.check_membership_expiry_warning(current_merchant)

    return success_response(
        data={
            "id": str(current_merchant.id),  # 转换为字符串，避免前端精度丢失
            "username": current_merchant.username,
            "shop_name": current_merchant.shop_name,
            "phone": current_merchant.phone,
            "address": current_merchant.address,
            "business_hours": current_merchant.business_hours,
            "qrcode_url": current_merchant.qrcode_url,
            "shop_id": current_merchant.shop_id,
            "share_link": current_merchant.share_link,
            "membership_expiry": current_merchant.membership_expiry,
            "is_membership_expired": is_membership_expired,
            "show_expiry_warning": show_expiry_warning,
            "status": current_merchant.status,
            "created_at": current_merchant.created_at,
            "updated_at": current_merchant.updated_at,
        },
        message="success",
    )


@router.put("/auth/me")
async def update_current_user(
    update_data: MerchantUpdate,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    更新当前用户信息

    更新当前登录商家的店铺信息
    """
    logger.info(f"商家更新信息请求: id={current_merchant.id}")

    merchant = merchant_service.update(
        db=db,
        merchant=current_merchant,
        shop_name=update_data.shop_name,
        phone=update_data.phone,
        address=update_data.address,
        business_hours=update_data.business_hours,
    )

    logger.info(f"商家信息更新成功: id={merchant.id}")

    return success_response(
        data={
            "id": str(merchant.id),  # 转换为字符串，避免前端精度丢失
            "username": merchant.username,
            "shop_name": merchant.shop_name,
            "phone": merchant.phone,
            "address": merchant.address,
            "business_hours": merchant.business_hours,
            "qrcode_url": merchant.qrcode_url,
            "shop_id": merchant.shop_id,
            "share_link": merchant.share_link,
            "status": merchant.status,
            "updated_at": merchant.updated_at,
        },
        message="更新成功",
    )


@router.put("/auth/password")
async def update_password(
    password_data: PasswordUpdateRequest,
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    """
    修改密码

    修改当前登录商家的密码
    """
    logger.info(f"商家修改密码请求: id={current_merchant.id}")

    # 验证旧密码
    if not verify_password(password_data.old_password, current_merchant.password_hash):
        raise InvalidCredentialsException(message="旧密码错误")

    # 更新密码
    merchant = merchant_service.update_password(
        db=db,
        merchant=current_merchant,
        new_password=password_data.new_password,
    )

    logger.info(f"商家密码修改成功: id={merchant.id}")

    return success_response(
        data={"id": str(merchant.id), "updated_at": merchant.updated_at},  # 转换为字符串，避免前端精度丢失
        message="密码修改成功",
    )


@router.post("/auth/logout")
async def logout():
    """
    登出

    客户端需要删除本地存储的Token
    """
    # JWT是无状态的，登出操作在客户端完成（删除Token）
    return success_response(message="登出成功")


@router.post("/auth/membership/renew")
async def renew_membership(
    renewal_data: MembershipRenewalRequest,
    current_merchant: Merchant = Depends(get_current_merchant_optional_membership),
    db: Session = Depends(get_db),
):
    """
    会员续期

    续期会员账号
    """
    logger.info(f"会员续期请求: id={current_merchant.id}, days={renewal_data.days}")

    merchant = merchant_service.renew_membership(
        db=db,
        merchant=current_merchant,
        days=renewal_data.days,
    )

    logger.info(f"会员续期成功: id={merchant.id}, expiry={merchant.membership_expiry}")

    return success_response(
        data={
            "membership_expiry": merchant.membership_expiry,
        },
        message="续期成功",
    )
