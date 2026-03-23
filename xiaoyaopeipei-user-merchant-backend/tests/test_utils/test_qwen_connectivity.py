"""
通义千问 + LangChain 连通性测试（简化版）

测试内容：
1. 发送简单请求
2. 验证响应

运行方式：
    cd xiaoyaopeipei-user-merchant-backend
    python tests/test_utils/test_qwen_connectivity.py
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.services.ai.llm import get_llm_client
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class TestQwenConnectivity:
    """通义千问连通性测试"""

    def check_config(self):
        """检查配置"""
        print("\n" + "=" * 60)
        print("通义千问 + LangChain 连通性测试")
        print("=" * 60)

        print("\n检查通义千问配置:")
        print(f"  QWEN_MODEL: {settings.QWEN_MODEL}")

        if not settings.QWEN_API_KEY or settings.QWEN_API_KEY == "sk-xxxxxxxxxxxxxxxx":
            print("\n✗ 通义千问API Key未配置")
            print("  请在.env.development中配置:")
            print("  - QWEN_API_KEY")
            return False

        return True

    def test_simple_chat(self):
        """测试简单对话"""
        print("\n[测试] 发送测试消息")
        try:
            llm_client = get_llm_client()

            messages = [
                {"role": "user", "content": "请回复：helloword"}
            ]

            print(f"  发送: 请回复：helloword")

            response = llm_client.chat(messages=messages)

            print(f"  ✓ 响应: {response}")
            print(f"  ✓ 连通成功")

            return True
        except Exception as e:
            print(f"  ✗ 请求失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_all_tests(self):
        """运行所有测试"""
        if not self.check_config():
            return False

        try:
            self.test_simple_chat()
            print("\n" + "=" * 60)
            print("✓ 通义千问测试通过！")
            print("=" * 60)
            return True
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            return False


def run_tests():
    """直接运行测试"""
    test_instance = TestQwenConnectivity()
    return test_instance.run_all_tests()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
