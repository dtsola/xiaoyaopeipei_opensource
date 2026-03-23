"""
对话记忆管理 - 混合方案：LangChain 记忆 + 数据库持久化

功能：
1. 使用 LangChain 管理对话上下文（用于 AI）
2. 数据库持久化所有消息（用于商户端线索展示）
3. Token 限制管理，自动裁剪旧消息
"""
from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.models.message import Message

logger = get_logger(__name__)


class ConversationMemory:
    """
    对话记忆管理器

    混合方案：
    - 内存缓存：用于 AI 上下文管理
    - 数据库：用于持久化（商户端线索展示）
    """

    def __init__(
        self,
        conversation_id: int,
        db: Session,
        max_messages: int = 10,
        max_tokens: int = 3000,
    ):
        """
        初始化对话记忆

        Args:
            conversation_id: 对话ID
            db: 数据库会话
            max_messages: 最大消息数量（用于 AI 上下文）
            max_tokens: 最大 token 数量（用于 AI 上下文）
        """
        self.conversation_id = conversation_id
        self.db = db
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self._messages: List[BaseMessage] = []
        self._loaded = False

    @property
    def messages(self) -> List[BaseMessage]:
        """获取消息列表（自动加载）"""
        if not self._loaded:
            self.load_from_db()
        return self._messages.copy()

    def load_from_db(self, limit: Optional[int] = None) -> None:
        """
        从数据库加载历史消息

        Args:
            limit: 加载的消息数量限制，None 表示使用 max_messages
        """
        try:
            limit = limit or self.max_messages
            messages = self.db.query(Message).filter(
                Message.conversation_id == self.conversation_id
            ).order_by(Message.created_at.desc()).limit(limit).all()

            # 按时间正序排列
            messages.reverse()

            self._messages = []
            for msg in messages:
                if msg.role == "user":
                    self._messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    self._messages.append(AIMessage(content=msg.content))

            self._loaded = True
            logger.debug(
                f"[Memory] 加载了 {len(self._messages)} 条历史消息 "
                f"(conversation_id={self.conversation_id})"
            )

        except Exception as e:
            logger.error(f"[Memory] 加载历史消息失败: {e}")
            self._messages = []
            self._loaded = True

    def add_user_message(self, content: str) -> None:
        """添加用户消息到内存"""
        self._messages.append(HumanMessage(content=content))
        self._trim_if_needed()

    def add_assistant_message(self, content: str) -> None:
        """添加 AI 消息到内存"""
        self._messages.append(AIMessage(content=content))
        self._trim_if_needed()

    def _trim_if_needed(self) -> None:
        """如果超过限制，裁剪旧消息"""
        # 方式1：按消息数量裁剪
        while len(self._messages) > self.max_messages:
            removed = self._messages.pop(0)
            logger.debug(f"[Memory] 移除旧消息（消息数量限制）: {removed.content[:50]}...")

        # 方式2：按 token 数量裁剪
        while self._estimate_tokens() > self.max_tokens and len(self._messages) > 2:
            removed = self._messages.pop(0)
            logger.debug(
                f"[Memory] 移除旧消息（token 限制）: {removed.content[:50]}... "
                f"(当前约 {self._estimate_tokens()} tokens)"
            )

    def _estimate_tokens(self) -> int:
        """
        估算当前消息的 token 数

        粗略估算：
        - 中文字符: ~1.5 tokens/字符
        - 英文字符: ~0.25 tokens/字符
        - 空格标点: ~0.1 tokens/字符
        """
        text = "\n".join([m.content for m in self._messages])

        # 统计中文字符
        chinese_chars = len([c for c in text if "\u4e00" <= c <= "\u9fff"])
        # 统计英文字符
        english_chars = len([c for c in text if c.isascii() and c.isalpha()])
        # 统计其他字符（空格、标点等）
        other_chars = len(text) - chinese_chars - english_chars

        return int(chinese_chars * 1.5 + english_chars * 0.25 + other_chars * 0.1)

    def get_llamaindex_context(self) -> str:
        """
        获取用于 LLM 的上下文字符串

        Returns:
            格式化的对话历史字符串
        """
        context_parts = []
        for msg in self._messages:
            if isinstance(msg, HumanMessage):
                context_parts.append(f"用户: {msg.content}")
            elif isinstance(msg, AIMessage):
                context_parts.append(f"助手: {msg.content}")

        return "\n".join(context_parts)

    def get_langchain_messages(self) -> List[BaseMessage]:
        """
        获取用于 LangChain 的消息列表

        Returns:
            LangChain 格式的消息列表
        """
        return self.messages.copy()

    def get_dict_messages(self) -> List[Dict[str, str]]:
        """
        获取字典格式的消息列表（用于 API）

        Returns:
            [{"role": "user", "content": "..."}, ...]
        """
        result = []
        for msg in self._messages:
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                result.append({"role": "system", "content": msg.content})
        return result

    def get_recent_summary(self, max_summary_messages: int = 3) -> str:
        """
        获取最近消息的摘要（用于 prompt）

        Args:
            max_summary_messages: 摘要的消息数量

        Returns:
            摘要字符串
        """
        recent = self._messages[-max_summary_messages:]
        if not recent:
            return "暂无对话历史"

        summary_parts = []
        for msg in recent:
            if isinstance(msg, HumanMessage):
                content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                summary_parts.append(f"用户: {content}")
            elif isinstance(msg, AIMessage):
                content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                summary_parts.append(f"AI: {content}")

        return "\n".join(summary_parts)

    def clear(self) -> None:
        """清除内存中的消息"""
        self._messages.clear()
        self._loaded = False

    def __len__(self) -> int:
        """返回消息数量"""
        return len(self._messages)

    def __repr__(self) -> str:
        return f"ConversationMemory(conversation_id={self.conversation_id}, messages={len(self._messages)})"


class MemoryManager:
    """
    记忆管理器（单例）

    管理多个对话的记忆，提供缓存和清理功能
    """

    _instance: Optional["MemoryManager"] = None
    _memories: Dict[int, ConversationMemory] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def get_memory(
        conversation_id: int,
        db: Session,
        max_messages: int = 10,
        max_tokens: int = 3000,
    ) -> ConversationMemory:
        """
        获取或创建对话记忆

        Args:
            conversation_id: 对话ID
            db: 数据库会话
            max_messages: 最大消息数量
            max_tokens: 最大 token 数量

        Returns:
            ConversationMemory 实例
        """
        if conversation_id not in MemoryManager._memories:
            MemoryManager._memories[conversation_id] = ConversationMemory(
                conversation_id=conversation_id,
                db=db,
                max_messages=max_messages,
                max_tokens=max_tokens,
            )
            logger.debug(f"[MemoryManager] 创建新记忆: conversation_id={conversation_id}")

        return MemoryManager._memories[conversation_id]

    @staticmethod
    def remove_memory(conversation_id: int) -> None:
        """移除对话记忆（释放内存）"""
        if conversation_id in MemoryManager._memories:
            del MemoryManager._memories[conversation_id]
            logger.debug(f"[MemoryManager] 移除记忆: conversation_id={conversation_id}")

    @staticmethod
    def clear_all() -> None:
        """清除所有记忆"""
        count = len(MemoryManager._memories)
        MemoryManager._memories.clear()
        logger.info(f"[MemoryManager] 清除所有记忆: {count} 个")

    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """获取记忆统计信息"""
        return {
            "total_conversations": len(MemoryManager._memories),
            "conversation_ids": list(MemoryManager._memories.keys()),
        }


# 便捷函数
def get_conversation_memory(
    conversation_id: int,
    db: Session,
    max_messages: int = 10,
    max_tokens: int = 3000,
) -> ConversationMemory:
    """
    获取对话记忆（便捷函数）

    Args:
        conversation_id: 对话ID
        db: 数据库会话
        max_messages: 最大消息数量
        max_tokens: 最大 token 数量

    Returns:
        ConversationMemory 实例
    """
    return MemoryManager.get_memory(
        conversation_id=conversation_id,
        db=db,
        max_messages=max_messages,
        max_tokens=max_tokens,
    )
