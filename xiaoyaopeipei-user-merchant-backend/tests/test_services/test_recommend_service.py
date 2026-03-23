"""
推荐理由生成服务测试
"""
import pytest
from unittest.mock import Mock, patch

from app.services.ai.recommend_service import RecommendReasonService


class MockSKU:
    """模拟SKU对象"""
    def __init__(self):
        self.id = 1
        self.name = "游戏本RTX4060"
        self.brand = "联想"
        self.price = 5999
        self.cpu = "i5-12450HX"
        self.gpu = "RTX 4060"
        self.ram = "16GB"
        self.storage = "512GB SSD"
        self.screen = "15.6英寸 144Hz"
        self.weight = "2.2kg"
        self.battery = None


class TestRecommendReasonService:
    """推荐理由生成服务测试"""

    @pytest.fixture
    def service(self):
        """创建服务实例"""
        return RecommendReasonService()

    @pytest.fixture
    def mock_sku(self):
        """创建模拟SKU"""
        return MockSKU()

    @pytest.fixture
    def user_needs(self):
        """用户需求"""
        return {
            "budget": "5000-7000",
            "device_type": "laptop",
            "usage": "游戏",
            "brand": "联想",
            "portable": None,
            "requirements": None,
        }

    def test_format_user_needs_complete(self, service, user_needs):
        """测试格式化完整用户需求"""
        result = service._format_user_needs(user_needs)
        assert "预算5000-7000元" in result
        assert "设备类型笔记本" in result
        assert "用途游戏" in result
        assert "偏好联想品牌" in result

    def test_format_user_needs_empty(self, service):
        """测试格式化空需求"""
        result = service._format_user_needs({})
        assert result == "无特殊需求"

    def test_format_sku_specs_complete(self, service, mock_sku):
        """测试格式化完整SKU配置"""
        result = service._format_sku_specs(mock_sku)
        assert "屏幕15.6英寸 144Hz" in result
        assert "重量2.2kg" in result

    def test_format_sku_specs_empty(self, service):
        """测试格式化空SKU配置"""
        mock_sku = Mock()
        mock_sku.screen = None
        mock_sku.weight = None
        mock_sku.battery = None
        result = service._format_sku_specs(mock_sku)
        assert result == "无"

    def test_fallback_reason(self, service, mock_sku, user_needs):
        """测试降级推荐理由生成"""
        result = service._fallback_reason(mock_sku, user_needs, 85)
        assert isinstance(result, str)
        assert len(result) > 10
        # 应该包含价格、用途、品牌等信息
        assert "5999" in result or "联想" in result or "游戏" in result

    @patch('app.services.ai.recommend_service.get_llm_client')
    def test_generate_reason_success(self, mock_llm, service, mock_sku, user_needs):
        """测试成功生成AI推荐理由"""
        # 模拟LLM返回
        mock_llm.return_value.chat.return_value = "  这是一台非常适合游戏玩家的高性能笔记本，配备RTX 4060显卡和i5处理器，完全满足您的游戏需求，而且价格在预算范围内。  "

        result = service.generate_reason(mock_sku, user_needs, 85)

        # 验证返回结果
        assert isinstance(result, str)
        assert len(result) > 0
        assert result.strip() == result  # 应该去除首尾空格

    @patch('app.services.ai.recommend_service.get_llm_client')
    def test_generate_reason_llm_failure_fallback(self, mock_llm, service, mock_sku, user_needs):
        """测试LLM失败时降级到模板"""
        # 模拟LLM抛出异常
        mock_llm.return_value.chat.side_effect = Exception("LLM服务不可用")

        result = service.generate_reason(mock_sku, user_needs, 85)

        # 应该返回降级理由
        assert isinstance(result, str)
        assert len(result) > 10

    def test_generate_reason_with_no_gpu(self, service, mock_sku, user_needs):
        """测试无显卡时的降级理由"""
        mock_sku.gpu = None
        user_needs_simple = {"usage": "办公"}

        result = service._fallback_reason(mock_sku, user_needs_simple, 70)
        assert isinstance(result, str)
        # 不应该有"显卡"相关描述
        assert "显卡" not in result

    def test_generate_reason_low_score(self, service, mock_sku, user_needs):
        """测试低分数时的降级理由"""
        result = service._fallback_reason(mock_sku, user_needs, 60)
        assert isinstance(result, str)
        # 低分数不应该有"高达"的描述
        assert "高达" not in result
