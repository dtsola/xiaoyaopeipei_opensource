"""
API依赖注入
"""
from typing import Optional, Generator
from datetime import datetime
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_token
from app.models.merchant import Merchant
from app.core.exceptions import MembershipExpiredException


def get_current_merchant(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[Merchant]:
    """
    获取当前登录商家（B端接口使用）

    Args:
        authorization: Authorization请求头
        db: 数据库会话

    Returns:
        当前商家对象

    Raises:
        HTTPException: 未授权
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证Token",
        )

    # 解析Bearer Token
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Token格式",
        )

    token = authorization.split(" ")[1]

    # 验证Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期",
        )

    merchant_id = payload.get("sub")
    if not merchant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效",
        )

    # 查询商家
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="商家不存在",
        )

    if merchant.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )

    # 检查会员是否过期
    if merchant.membership_expiry and merchant.membership_expiry < datetime.now():
        raise MembershipExpiredException()

    return merchant


def get_current_merchant_optional_membership(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[Merchant]:
    """
    获取当前登录商家（不检查会员过期状态）

    用于登录、获取用户信息、会员续期等接口
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证Token",
        )

    # 解析Bearer Token
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Token格式",
        )

    token = authorization.split(" ")[1]

    # 验证Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期",
        )

    merchant_id = payload.get("sub")
    if not merchant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效",
        )

    # 查询商家
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="商家不存在",
        )

    if merchant.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )

    return merchant


# 可选的认证（游客模式）
async def get_optional_merchant(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[Merchant]:
    """
    获取当前商家（可选，未登录返回None）
    """
    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if not payload:
        return None

    merchant_id = payload.get("sub")
    if not merchant_id:
        return None

    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    return merchant
