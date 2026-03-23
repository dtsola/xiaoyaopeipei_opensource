"""
消息服务
"""
import json
from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.message import Message
from app.utils.snowflake import generate_id


class MessageService:
    """消息服务类"""

    def get_by_id(self, db: Session, id: int) -> Optional[Message]:
        """根据ID获取消息"""
        return db.query(Message).filter(Message.id == id).first()

    def get_by_conversation(
        self,
        db: Session,
        conversation_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Message]:
        """
        获取对话的消息列表

        Args:
            db: 数据库会话
            conversation_id: 对话ID
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            消息列表（按时间升序）
        """
        query = db.query(Message).filter(
            Message.conversation_id == conversation_id
        )

        return (
            query.order_by(Message.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self,
        db: Session,
        *,
        conversation_id: int,
        role: str,
        content: str,
        extracted_info: Optional[dict] = None,
        confidence: Optional[float] = None,
    ) -> Message:
        """
        创建消息

        Args:
            db: 数据库会话
            conversation_id: 对话ID
            role: 角色（user/assistant）
            content: 消息内容
            extracted_info: AI提取的信息（JSON）
            confidence: 置信度

        Returns:
            创建的消息对象
        """
        # 生成雪花ID
        message_id = generate_id()

        # 处理JSON字段
        extracted_info_json = (
            json.dumps(extracted_info, ensure_ascii=False)
            if extracted_info
            else None
        )

        message = Message(
            id=message_id,
            conversation_id=conversation_id,
            role=role,
            content=content,
            extracted_info=extracted_info_json,
            confidence=confidence,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def create_user_message(
        self,
        db: Session,
        *,
        conversation_id: int,
        content: str,
    ) -> Message:
        """
        创建用户消息

        Args:
            db: 数据库会话
            conversation_id: 对话ID
            content: 消息内容

        Returns:
            创建的消息对象
        """
        return self.create(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

    def create_assistant_message(
        self,
        db: Session,
        *,
        conversation_id: int,
        content: str,
        extracted_info: Optional[dict] = None,
        confidence: Optional[float] = None,
    ) -> Message:
        """
        创建AI助手消息

        Args:
            db: 数据库会话
            conversation_id: 对话ID
            content: 消息内容
            extracted_info: AI提取的信息（JSON）
            confidence: 置信度

        Returns:
            创建的消息对象
        """
        return self.create(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            extracted_info=extracted_info,
            confidence=confidence,
        )

    def get_conversation_history(
        self,
        db: Session,
        conversation_id: int,
        limit: int = 20,
    ) -> List[dict]:
        """
        获取对话历史（用于AI上下文）

        Args:
            db: 数据库会话
            conversation_id: 对话ID
            limit: 返回消息数量

        Returns:
            消息字典列表
        """
        messages = self.get_by_conversation(
            db=db,
            conversation_id=conversation_id,
            limit=limit,
        )

        return [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in messages
        ]


# 创建服务实例
message_service = MessageService()
