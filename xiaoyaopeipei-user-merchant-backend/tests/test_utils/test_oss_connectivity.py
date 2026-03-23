"""
阿里云OSS连通性测试（简化版）

测试内容：
1. 上传测试文件
2. 验证上传成功

运行方式：
    cd xiaoyaopeipei-user-merchant-backend
    python tests/test_utils/test_oss_connectivity.py
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.utils.oss import get_oss_client
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class TestOSSConnectivity:
    """OSS连通性测试"""

    def check_config(self):
        """检查配置"""
        print("\n" + "=" * 60)
        print("OSS连通性测试")
        print("=" * 60)

        print("\n检查OSS配置:")
        print(f"  OSS_ENDPOINT: {settings.OSS_ENDPOINT}")
        print(f"  OSS_BUCKET: {settings.OSS_BUCKET}")

        if not all([
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET,
            settings.OSS_BUCKET
        ]):
            print("\n✗ OSS配置不完整")
            print("  请在.env.development中配置:")
            print("  - OSS_ACCESS_KEY_ID")
            print("  - OSS_ACCESS_KEY_SECRET")
            print("  - OSS_BUCKET")
            return False

        return True

    def test_upload_file(self):
        """测试上传文件"""
        print("\n[测试] 上传测试文件")
        try:
            oss_client = get_oss_client()

            # 创建测试文件
            test_content = b"helloword"
            test_filename = oss_client.generate_filename("test.txt", prefix="connectivity-test")

            print(f"  文件名: {test_filename}")
            print(f"  内容: helloword")

            # 上传文件
            file_url = oss_client.upload_file(
                file_content=test_content,
                filename=test_filename,
                content_type="text/plain"
            )

            print(f"  ✓ 上传成功")
            print(f"  ✓ 文件URL: {file_url}")

            # 保存文件名用于清理
            self.test_filename = test_filename

            return True
        except Exception as e:
            print(f"  ✗ 上传失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_cleanup(self):
        """清理测试文件"""
        try:
            if hasattr(self, 'test_filename'):
                oss_client = get_oss_client()
                oss_client.delete_file(self.test_filename)
                print(f"  ✓ 测试文件已清理")
        except:
            pass

    def run_all_tests(self):
        """运行所有测试"""
        if not self.check_config():
            return False

        try:
            self.test_upload_file()
            print("\n" + "=" * 60)
            print("✓ OSS测试通过！")
            print("=" * 60)
            return True
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            return False
        finally:
            self.test_cleanup()


def run_tests():
    """直接运行测试"""
    test_instance = TestOSSConnectivity()
    return test_instance.run_all_tests()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
