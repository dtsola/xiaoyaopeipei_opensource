"""
对话记忆功能测试
"""
import pytest
from sqlalchemy.orm import Session

from app.services.ai.memory import (
    ConversationMemory,
    MemoryManager,
    get_conversation_memory,
)


class TestConversationMemory:
    """对话记忆测试"""

    def test_memory_init(self, db: Session):
        """测试记忆初始化"""
        memory = ConversationMemory(
            conversation_id=1,
            db=db,
            max_messages=10,
            max_tokens=3000,
        )
        assert memory.conversation_id == 1
        assert memory.max_messages == 10
        assert memory.max_tokens == 3000
        assert len(memory) == 0

    def test_add_user_message(self, db: Session):
        """测试添加用户消息"""
        memory = ConversationMemory(
            conversation_id=1,
            db=db,
        )
        memory.add_user_message("你好")
        memory.add_user_message("我需要一台电脑")

        assert len(memory) == 2

    def test_add_assistant_message(self, db: Session):
        """测试添加AI消息"""
        memory = ConversationMemory(
            conversation_id=1,
            db=db,
        )
        memory.add_assistant_message("您好！我可以帮您选择电脑")
        memory.add_assistant_message("请问您的预算是多少？")

        assert len(memory) == 2

    def test_trim_by_message_count(self, db: Session):
        """测试按消息数量裁剪"""
        memory = ConversationMemory(
            conversation_id=1,
            db=db,
            max_messages=5,
        )

        # 添加10条消息
        for i in range(10):
            if i % 2 == 0:
                memory.add_user_message(f"用户消息{i}")
            else:
                memory.add_assistant_message(f"AI消息{i}")

        # 应该只保留最后5条
        assert len(memory) == 5

    def test_get_dict_messages(self, db: Session):
        """测试获取字典格式消息"""
        memory = ConversationMemory(
            conversation_id=1,
            db=db,
        )
        memory.add_user_message("你好")
        memory.add_assistant_message("您好！")

        messages = memory.get_dict_messages()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "你好"
        assert messages[1]["role"] == "assistant"
        assert messages[1]["content"] == "您好！"


class TestMemoryManager:
    """记忆管理器测试"""

    def test_get_memory(self, db: Session):
        """测试获取记忆"""
        memory1 = MemoryManager.get_memory(conversation_id=1, db=db)
        memory2 = MemoryManager.get_memory(conversation_id=1, db=db)

        # 应该返回同一个实例
        assert memory1 is memory2

    def test_different_conversations(self, db: Session):
        """测试不同对话的记忆"""
        memory1 = MemoryManager.get_memory(conversation_id=1, db=db)
        memory2 = MemoryManager.get_memory(conversation_id=2, db=db)

        # 应该是不同的实例
        assert memory1 is not memory2
        assert memory1.conversation_id == 1
        assert memory2.conversation_id == 2

    def test_remove_memory(self, db: Session):
        """测试移除记忆"""
        MemoryManager.get_memory(conversation_id=1, db=db)
        MemoryManager.remove_memory(conversation_id=1)

        # 再次获取应该是新实例
        memory1 = MemoryManager.get_memory(conversation_id=1, db=db)
        MemoryManager.remove_memory(conversation_id=1)
        memory2 = MemoryManager.get_memory(conversation_id=1, db=db)

        assert memory1 is not memory2

    def test_clear_all(self, db: Session):
        """测试清除所有记忆"""
        MemoryManager.get_memory(conversation_id=1, db=db)
        MemoryManager.get_memory(conversation_id=2, db=db)

        stats = MemoryManager.get_stats()
        assert stats["total_conversations"] >= 2

        MemoryManager.clear_all()

        stats = MemoryManager.get_stats()
        assert stats["total_conversations"] == 0

    def test_get_stats(self, db: Session):
        """测试获取统计信息"""
        MemoryManager.clear_all()

        MemoryManager.get_memory(conversation_id=1, db=db)
        MemoryManager.get_memory(conversation_id=2, db=db)

        stats = MemoryManager.get_stats()
        assert stats["total_conversations"] == 2
        assert 1 in stats["conversation_ids"]
        assert 2 in stats["conversation_ids"]


class TestConvenienceFunction:
    """便捷函数测试"""

    def test_get_conversation_memory(self, db: Session):
        """测试便捷函数"""
        memory = get_conversation_memory(
            conversation_id=1,
            db=db,
            max_messages=5,
        )

        assert memory.conversation_id == 1
        assert memory.max_messages == 5
