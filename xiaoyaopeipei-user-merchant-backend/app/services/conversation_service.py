"""
对话服务
"""
import json
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.conversation import Conversation
from app.utils.snowflake import generate_id


class ConversationService:
    """对话服务类"""

    def get_by_id(self, db: Session, id: int) -> Optional[Conversation]:
        """根据ID获取对话"""
        return db.query(Conversation).filter(Conversation.id == id).first()

    def get_by_session_id(self, db: Session, session_id: str) -> Optional[Conversation]:
        """根据session_id获取对话"""
        return db.query(Conversation).filter(Conversation.session_id == session_id).first()

    def get_by_merchant(
        self,
        db: Session,
        merchant_id: int,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
    ) -> tuple[List[Conversation], int]:
        """
        获取商家的对话列表

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            skip: 跳过记录数
            limit: 返回记录数
            status: 状态筛选

        Returns:
            (对话列表, 总数)
        """
        query = db.query(Conversation).filter(Conversation.merchant_id == merchant_id)

        if status:
            query = query.filter(Conversation.status == status)

        # 获取总数
        total = query.count()

        # 分页查询
        items = (
            query.order_by(Conversation.created_at.desc())
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
        session_id: Optional[str] = None,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Conversation:
        """
        创建对话

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            session_id: 会话ID（如不传则自动生成）
            client_ip: 客户端IP
            user_agent: 浏览器信息
            source: 来源

        Returns:
            创建的对话对象
        """
        # 生成雪花ID
        conversation_id = generate_id()

        # 生成session_id
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:16]}"

        conversation = Conversation(
            id=conversation_id,
            merchant_id=merchant_id,
            session_id=session_id,
            client_ip=client_ip,
            user_agent=user_agent,
            source=source,
            status="active",
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def update_status(
        self,
        db: Session,
        *,
        conversation: Conversation,
        status: str,
    ) -> Conversation:
        """
        更新对话状态

        Args:
            db: 数据库会话
            conversation: 对话对象
            status: 新状态（active/completed/abandoned）

        Returns:
            更新后的对话对象
        """
        conversation.status = status
        db.commit()
        db.refresh(conversation)
        return conversation

    def get_or_create_by_session(
        self,
        db: Session,
        *,
        merchant_id: int,
        session_id: Optional[str],
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Conversation:
        """
        根据session_id获取对话，不存在则创建

        Args:
            db: 数据库会话
            merchant_id: 商家ID
            session_id: 会话ID
            client_ip: 客户端IP
            user_agent: 浏览器信息
            source: 来源

        Returns:
            对话对象
        """
        if session_id:
            conversation = self.get_by_session_id(db, session_id=session_id)
            if conversation:
                # 验证是否属于同一商家
                if conversation.merchant_id != merchant_id:
                    # session_id与商家不匹配，创建新对话
                    conversation = self.create(
                        db=db,
                        merchant_id=merchant_id,
                        client_ip=client_ip,
                        user_agent=user_agent,
                        source=source,
                    )
                return conversation

        # 创建新对话
        return self.create(
            db=db,
            merchant_id=merchant_id,
            session_id=session_id,
            client_ip=client_ip,
            user_agent=user_agent,
            source=source,
        )

    def verify_ownership(
        self, db: Session, *, conversation_id: int, merchant_id: int
    ) -> bool:
        """
        验证对话是否属于指定商家

        Args:
            db: 数据库会话
            conversation_id: 对话ID
            merchant_id: 商家ID

        Returns:
            是否属于该商家
        """
        conversation = self.get_by_id(db, id=conversation_id)
        return conversation is not None and conversation.merchant_id == merchant_id


# 创建服务实例
conversation_service = ConversationService()
