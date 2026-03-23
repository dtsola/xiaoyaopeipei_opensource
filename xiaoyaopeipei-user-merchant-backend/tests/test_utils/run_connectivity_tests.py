"""
第三方服务连通性综合测试（简化版）

一键测试所有外部服务的连通性：
1. 阿里云OSS
2. 通义千问 + LangChain

运行方式：
    cd xiaoyaopeipei-user-merchant-backend
    python tests/test_utils/run_connectivity_tests.py
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tests.test_utils.test_oss_connectivity import TestOSSConnectivity
from tests.test_utils.test_qwen_connectivity import TestQwenConnectivity

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_summary(results):
    """打印测试结果汇总"""
    print("\n" + "=" * 70)
    print("  测试结果汇总")
    print("=" * 70)

    total = len([r for r in results if r["success"] is not None])
    passed = sum(1 for r in results if r["success"] is True)
    failed = sum(1 for r in results if r["success"] is False)
    skipped = sum(1 for r in results if r["success"] is None)

    for result in results:
        if result["success"] is None:
            status = "⊘ 跳过"
        elif result["success"]:
            status = "✓ 通过"
        else:
            status = "✗ 失败"
        print(f"  {result['name']:30s} {status}")

    print("\n" + "-" * 70)
    print(f"  总计: {total}  |  通过: {passed}  |  失败: {failed}  |  跳过: {skipped}")
    print("=" * 70)

    return failed == 0


def main():
    """主函数"""
    print_header("小遥配配 - 第三方服务连通性测试")

    # 显示配置信息
    print("\n当前配置:")
    print(f"  环境: {settings.APP_ENV}")
    print(f"  调试模式: {settings.APP_DEBUG}")

    print("\nOSS配置:")
    oss_configured = bool(settings.OSS_ACCESS_KEY_ID and settings.OSS_ACCESS_KEY_SECRET and settings.OSS_BUCKET)
    print(f"  状态: {'已配置' if oss_configured else '未配置'}")
    if oss_configured:
        print(f"  Bucket: {settings.OSS_BUCKET}")
        print(f"  Endpoint: {settings.OSS_ENDPOINT}")

    print("\n通义千问配置:")
    qwen_configured = bool(settings.QWEN_API_KEY and settings.QWEN_API_KEY != "sk-xxxxxxxxxxxxxxxx")
    print(f"  状态: {'已配置' if qwen_configured else '未配置'}")
    if qwen_configured:
        print(f"  模型: {settings.QWEN_MODEL}")

    results = []

    # OSS连通性测试
    if oss_configured:
        try:
            print_header("1. 阿里云OSS连通性测试")
            test = TestOSSConnectivity()
            success = test.run_all_tests()
            results.append({"name": "阿里云OSS", "success": success})
        except Exception as e:
            print(f"\n✗ OSS测试异常: {e}")
            import traceback
            traceback.print_exc()
            results.append({"name": "阿里云OSS", "success": False})
    else:
        print("\n[跳过] OSS未配置，跳过OSS连通性测试")
        results.append({"name": "阿里云OSS", "success": None})

    # 通义千问连通性测试
    if qwen_configured:
        try:
            print_header("2. 通义千问 + LangChain 连通性测试")
            test = TestQwenConnectivity()
            success = test.run_all_tests()
            results.append({"name": "通义千问", "success": success})
        except Exception as e:
            print(f"\n✗ 通义千问测试异常: {e}")
            import traceback
            traceback.print_exc()
            results.append({"name": "通义千问", "success": False})
    else:
        print("\n[跳过] 通义千问未配置，跳过连通性测试")
        results.append({"name": "通义千问", "success": None})

    # 打印汇总
    all_passed = print_summary(results)

    # 返回结果
    if all_passed:
        print("\n✓ 所有服务连通性测试通过！可以开始后续开发任务。")
        return 0
    else:
        print("\n✗ 部分服务测试失败，请检查配置后重试。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
