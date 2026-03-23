"""
线索服务
"""
import json
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from app.models.lead import Lead
from app.models.sku import Sku
from app.models.conversation import Conversation
from app.utils.snowflake import generate_id
from app.core.security import encrypt_data, decrypt_data, mask_phone


class LeadService:
    """线索服务类"""

    def get_by_id(self, db: Session, id: int | str) -> Optional[Lead]:
        """根据ID获取线索（支持字符串ID，自动转换为int）"""
        try:
            lead_id = int(id) if isinstance(id, str) else id
        except (ValueError, TypeError):
            return None
        return db.query(Lead).filter(Lead.id == lead_id).first()

    def get_by_conversation_id(
        self, db: Session, conversation_id: int
    ) -> Optional[Lead]:
        """根据对话ID获取线索"""
        return db.query(Lead).filter(Lead.conversation_id == conversation_id).first()

    def get_by_merchant(
        self,
        db: Session,
        merchant_id: int,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        device_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Lead], int]:
        """
        获取商家的线索列表

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            skip: 跳过记录数
            limit: 返回记录数
            status: 状态筛选
            device_type: 设备类型筛选
            start_date: 开始日期
            end_date: 结束日期
            search: 搜索关键词（手机号、备注）

        Returns:
            (线索列表, 总数)
        """
        # 构建查询
        query = db.query(Lead).filter(Lead.merchant_id == merchant_id)

        # 状态筛选
        if status:
            query = query.filter(Lead.status == status)

        # 设备类型筛选
        if device_type:
            query = query.filter(Lead.device_type == device_type)

        # 日期范围筛选
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                query = query.filter(Lead.created_at >= start_dt)
            except ValueError:
                pass

        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                # 包含当天
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Lead.created_at <= end_dt)
            except ValueError:
                pass

        # 搜索关键词
        if search:
            # 尝试解密手机号进行匹配
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Lead.remark.like(search_pattern),
                    Lead.requirements.like(search_pattern),
                )
            )

        # 获取总数
        total = query.count()

        # 分页查询（按创建时间倒序）
        items = (
            query.order_by(desc(Lead.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    def create(
        self,
        db: Session,
        *,
        merchant_id: int,
        conversation_id: int,
        phone: str,
        wechat: Optional[str] = None,
        remark: Optional[str] = None,
        budget: Optional[str] = None,
        device_type: Optional[str] = None,
        usage: Optional[str] = None,
        requirements: Optional[str] = None,
        selected_sku_id: Optional[int] = None,
    ) -> Lead:
        """
        创建线索

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            conversation_id: 对话ID
            phone: 手机号（明文）
            wechat: 微信号（明文）
            remark: 客户备注
            budget: 预算
            device_type: 设备类型
            usage: 用途
            requirements: 具体需求
            selected_sku_id: 选中的SKU ID

        Returns:
            创建的线索对象
        """
        # 生成雪花ID
        lead_id = generate_id()

        # 加密敏感信息
        encrypted_phone = encrypt_data(phone)
        encrypted_wechat = encrypt_data(wechat) if wechat else None

        lead = Lead(
            id=lead_id,
            merchant_id=merchant_id,
            conversation_id=conversation_id,
            phone=encrypted_phone,
            wechat=encrypted_wechat,
            remark=remark,
            budget=budget,
            device_type=device_type,
            usage=usage,
            requirements=requirements,
            selected_sku_id=selected_sku_id,
            status="pending",
            notes="[]",  # 初始化为空数组
        )

        db.add(lead)
        db.commit()
        db.refresh(lead)

        return lead

    def update_status(
        self,
        db: Session,
        *,
        lead: Lead,
        status: str,
    ) -> Lead:
        """
        更新线索状态

        Args:
            db: 数据库会话
            lead: 线索对象
            status: 新状态（pending/contacted/closed/abandoned）

        Returns:
            更新后的线索对象
        """
        lead.status = status
        db.commit()
        db.refresh(lead)
        return lead

    def add_note(
        self,
        db: Session,
        *,
        lead: Lead,
        content: str,
        merchant_id: int,
    ) -> Lead:
        """
        添加跟进记录

        Args:
            db: 数据库会话
            lead: 线索对象
            content: 跟进内容
            merchant_id: 商家ID

        Returns:
            更新后的线索对象
        """
        # 解析现有记录
        try:
            notes = json.loads(lead.notes) if lead.notes else []
        except:
            notes = []

        # 添加新记录
        note = {
            "id": generate_id(),
            "content": content,
            "created_by": merchant_id,
            "created_at": datetime.now().isoformat(),
        }
        notes.append(note)

        # 限制最多保留50条记录
        if len(notes) > 50:
            notes = notes[-50:]

        lead.notes = json.dumps(notes, ensure_ascii=False)
        db.commit()
        db.refresh(lead)

        return lead

    def get_lead_with_details(
        self, db: Session, lead_id: int | str, merchant_id: int
    ) -> Optional[dict]:
        """
        获取线索详情（包含关联信息）

        Args:
            db: 数据库会话
            lead_id: 线索ID（支持字符串类型）
            merchant_id: 商家ID

        Returns:
            线索详情字典
        """
        lead = self.get_by_id(db, id=lead_id)
        if not lead or lead.merchant_id != merchant_id:
            return None

        # 解密敏感信息
        phone = decrypt_data(lead.phone)
        wechat = decrypt_data(lead.wechat) if lead.wechat else None

        # 获取选中的SKU信息
        selected_sku = None
        if lead.selected_sku_id:
            sku = db.query(Sku).filter(Sku.id == lead.selected_sku_id).first()
            if sku:
                selected_sku = {
                    "id": str(sku.id),  # 转换为字符串，避免前端精度丢失
                    "name": sku.name,
                    "price": float(sku.price),
                }

        # 获取对话信息
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == lead.conversation_id)
            .first()
        )
        conversation_info = None
        if conversation:
            conversation_info = {
                "id": str(conversation.id),  # 转换为字符串，避免前端精度丢失
                "session_id": conversation.session_id,
                "status": conversation.status,
                "created_at": conversation.created_at.isoformat()
                if conversation.created_at
                else None,
            }

        # 解析跟进记录
        try:
            notes = json.loads(lead.notes) if lead.notes else []
        except:
            notes = []

        return {
            "id": str(lead.id),  # 转换为字符串，避免前端精度丢失
            "phone": phone,
            "wechat": wechat,
            "remark": lead.remark,
            "budget": lead.budget,
            "device_type": lead.device_type,
            "usage": lead.usage,
            "requirements": lead.requirements,
            "selected_sku": selected_sku,
            "conversation": conversation_info,
            "notes": notes,
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
            "updated_at": lead.updated_at.isoformat() if lead.updated_at else None,
        }

    def to_list_item(self, lead: Lead, include_decrypted_phone: bool = False) -> dict:
        """
        将线索对象转换为列表项字典

        Args:
            lead: 线索对象
            include_decrypted_phone: 是否包含解密后的手机号

        Returns:
            列表项字典
        """
        # 获取选中的SKU信息（需要传db，这里简化处理）
        selected_sku_info = None
        if lead.selected_sku_id:
            # 这里需要db session，实际使用时在外部处理
            selected_sku_info = {
                "id": lead.selected_sku_id,
                "name": "",
                "price": 0,
            }

        # 处理手机号：根据参数选择脱敏或解密
        if include_decrypted_phone:
            phone = decrypt_data(lead.phone)
        else:
            phone = mask_phone(lead.phone)

        # 处理微信号：根据参数选择解密或不显示
        if include_decrypted_phone and lead.wechat:
            wechat = decrypt_data(lead.wechat)
        else:
            wechat = None

        return {
            "id": lead.id,
            "phone": phone,
            "wechat": wechat,
            "budget": lead.budget,
            "device_type": lead.device_type,
            "usage": lead.usage,
            "requirements": lead.requirements,
            "selected_sku": selected_sku_info,
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        }

    def verify_ownership(self, db: Session, *, lead_id: int | str, merchant_id: int) -> bool:
        """
        验证线索是否属于指定商家

        Args:
            db: 数据库会话
            lead_id: 线索ID（支持字符串类型）
            merchant_id: 商家ID

        Returns:
            是否属于该商家
        """
        lead = self.get_by_id(db, id=lead_id)
        return lead is not None and lead.merchant_id == merchant_id


# 创建服务实例
lead_service = LeadService()
