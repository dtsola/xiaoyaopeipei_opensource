"""
商家服务
"""
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.merchant import Merchant
from app.core.security import hash_password, verify_password
from app.utils.snowflake import generate_id
from app.core.config import settings


class MerchantService:
    """商家服务类"""

    def get_by_id(self, db: Session, id: int) -> Optional[Merchant]:
        """根据ID获取商家"""
        return db.query(Merchant).filter(Merchant.id == id).first()

    def get_by_username(self, db: Session, username: str) -> Optional[Merchant]:
        """根据用户名获取商家"""
        return db.query(Merchant).filter(Merchant.username == username).first()

    def get_by_shop_id(self, db: Session, shop_id: str) -> Optional[Merchant]:
        """根据店铺ID获取商家"""
        return db.query(Merchant).filter(Merchant.shop_id == shop_id).first()

    def get_by_share_link(self, db: Session, share_link: str) -> Optional[Merchant]:
        """根据完整分享链接获取商家"""
        return db.query(Merchant).filter(Merchant.share_link == share_link).first()

    def create(
        self,
        db: Session,
        *,
        username: str,
        password: str,
        shop_name: str,
        phone: str,
        address: Optional[str] = None,
        business_hours: str = "9:00-21:00",
    ) -> Merchant:
        """
        创建商家

        Args:
            db: 数据库会话
            username: 用户名
            password: 明文密码
            shop_name: 店铺名称
            phone: 联系电话
            address: 店铺地址
            business_hours: 营业时间

        Returns:
            创建的商家对象
        """
        # 生成雪花ID
        merchant_id = generate_id()

        # 生成完整的分享链接（包含用户端域名）
        shop_id = f"shop_{merchant_id}"
        frontend_url = settings.USER_FRONTEND_URL_PROD if settings.APP_ENV == "production" else settings.USER_FRONTEND_URL
        share_link = f"{frontend_url}/?shop={shop_id}"

        # 计算会员到期时间（注册赠送默认天数）
        membership_expiry = datetime.now() + timedelta(days=settings.MEMBERSHIP_DEFAULT_DAYS)

        merchant = Merchant(
            id=merchant_id,
            username=username,
            password_hash=hash_password(password),
            shop_name=shop_name,
            phone=phone,
            address=address,
            business_hours=business_hours,
            shop_id=shop_id,
            share_link=share_link,
            membership_expiry=membership_expiry,
        )

        db.add(merchant)
        db.commit()
        db.refresh(merchant)

        return merchant

    def update(
        self,
        db: Session,
        *,
        merchant: Merchant,
        shop_name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        business_hours: Optional[str] = None,
    ) -> Merchant:
        """
        更新商家信息

        Args:
            db: 数据库会话
            merchant: 商家对象
            shop_name: 店铺名称
            phone: 联系电话
            address: 店铺地址
            business_hours: 营业时间

        Returns:
            更新后的商家对象
        """
        if shop_name is not None:
            merchant.shop_name = shop_name
        if phone is not None:
            merchant.phone = phone
        if address is not None:
            merchant.address = address
        if business_hours is not None:
            merchant.business_hours = business_hours

        db.commit()
        db.refresh(merchant)

        return merchant

    def update_password(
        self,
        db: Session,
        *,
        merchant: Merchant,
        new_password: str,
    ) -> Merchant:
        """
        更新商家密码

        Args:
            db: 数据库会话
            merchant: 商家对象
            new_password: 新密码（明文）

        Returns:
            更新后的商家对象
        """
        merchant.password_hash = hash_password(new_password)

        db.commit()
        db.refresh(merchant)

        return merchant

    def renew_membership(
        self,
        db: Session,
        *,
        merchant: Merchant,
        days: Optional[int] = None,
    ) -> Merchant:
        """
        续期会员

        Args:
            db: 数据库会话
            merchant: 商家对象
            days: 续期天数，默认使用配置的默认天数

        Returns:
            更新后的商家对象
        """
        if days is None:
            days = settings.MEMBERSHIP_DEFAULT_DAYS

        # 如果当前未过期，从到期时间开始计算；如果已过期，从现在开始计算
        base_time = merchant.membership_expiry if merchant.membership_expiry and merchant.membership_expiry > datetime.now() else datetime.now()
        merchant.membership_expiry = base_time + timedelta(days=days)

        db.commit()
        db.refresh(merchant)

        return merchant

    def check_membership_expiry_warning(self, merchant: Merchant) -> bool:
        """
        检查是否需要显示会员到期提醒

        Args:
            merchant: 商家对象

        Returns:
            True表示需要提醒，False表示不需要提醒
        """
        if not merchant.membership_expiry:
            return False

        days_remaining = (merchant.membership_expiry - datetime.now()).days
        return days_remaining <= settings.MEMBERSHIP_RENEWAL_THRESHOLD

    def authenticate(
        self,
        db: Session,
        *,
        username: str,
        password: str,
    ) -> Optional[Merchant]:
        """
        验证商家登录

        Args:
            db: 数据库会话
            username: 用户名
            password: 明文密码

        Returns:
            验证成功返回商家对象，失败返回None
        """
        merchant = self.get_by_username(db, username=username)
        if not merchant:
            return None

        if not verify_password(password, merchant.password_hash):
            return None

        if merchant.status != "active":
            return None

        return merchant

    def delete(self, db: Session, *, merchant: Merchant) -> Merchant:
        """
        删除商家（软删除）

        Args:
            db: 数据库会话
            merchant: 商家对象

        Returns:
            删除后的商家对象
        """
        # 软删除：更新状态为inactive
        merchant.status = "inactive"

        db.commit()
        db.refresh(merchant)

        return merchant


# 创建服务实例
merchant_service = MerchantService()
