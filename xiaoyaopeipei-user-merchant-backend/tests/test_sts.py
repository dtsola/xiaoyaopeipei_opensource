"""
STS 连通性测试

测试阿里云 STS 服务是否正常工作
"""
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def test_sts_import():
    """测试 STS SDK 导入"""
    print("\n=== 测试 1: STS SDK 导入 ===")
    try:
        from aliyunsdkcore.client import AcsClient
        from aliyunsdksts.request.v20150401 import AssumeRoleRequest
        from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
        print("✅ STS SDK 导入成功")
        return True
    except ImportError as e:
        print(f"❌ STS SDK 导入失败: {e}")
        return False


def test_sts_configuration():
    """测试 STS 配置"""
    print("\n=== 测试 2: STS 配置检查 ===")

    print(f"OSS_ACCESS_KEY_ID: {settings.OSS_ACCESS_KEY_ID[:10]}...")
    print(f"OSS_ACCESS_KEY_SECRET: {settings.OSS_ACCESS_KEY_SECRET[:10]}...")
    print(f"OSS_BUCKET: {settings.OSS_BUCKET}")
    print(f"OSS_REGION: {settings.OSS_REGION}")

    role_arn = getattr(settings, 'OSS_STS_ROLE_ARN', None)
    if role_arn:
        print(f"✅ OSS_STS_ROLE_ARN: {role_arn}")
    else:
        print("⚠️  OSS_STS_ROLE_ARN 未配置，将使用永久 AccessKey")

    return role_arn


def test_sts_get_credentials():
    """测试获取 STS 临时凭证"""
    print("\n=== 测试 3: 获取 STS 临时凭证 ===")

    role_arn = getattr(settings, 'OSS_STS_ROLE_ARN', None)

    if not role_arn:
        print("⚠️  未配置 OSS_STS_ROLE_ARN，跳过 STS 测试")
        return None

    try:
        from aliyunsdkcore.client import AcsClient
        from aliyunsdksts.request.v20150401 import AssumeRoleRequest

        # 创建 STS 客户端
        client = AcsClient(
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET,
            settings.OSS_REGION
        )

        # 创建 AssumeRole 请求
        request = AssumeRoleRequest.AssumeRoleRequest()
        request.set_RoleArn(role_arn)
        request.set_RoleSessionName("test-session")
        request.set_DurationSeconds(3600)

        print(f"正在调用 STS API...")
        print(f"  Role ARN: {role_arn}")
        print(f"  Session Name: test-session")
        print(f"  Duration: 3600秒")

        # 发送请求
        response = client.do_action_with_exception(request)

        # 解析响应
        import json
        result = json.loads(response.decode('utf-8'))

        print("\n✅ STS API 调用成功！")
        print(f"  RequestId: {result.get('RequestId')}")

        credentials = result.get('Credentials', {})
        print(f"\n临时凭证信息:")
        print(f"  AccessKeyId: {credentials.get('AccessKeyId', '')[:20]}...")
        print(f"  SecurityToken: {credentials.get('SecurityToken', '')[:30]}...")
        print(f"  Expiration: {credentials.get('Expiration')}")

        # 验证凭证完整性
        required_fields = ['AccessKeyId', 'AccessKeySecret', 'SecurityToken']
        missing_fields = [f for f in required_fields if not credentials.get(f)]

        if missing_fields:
            print(f"\n❌ 凭证不完整，缺少字段: {missing_fields}")
            return None

        if not missing_fields:
            print(f"\n✅ 凭证完整，所有必需字段都存在")

        return credentials

    except Exception as e:
        print(f"\n❌ STS API 调用失败: {e}")
        print("\n可能的原因:")
        print("  1. STS Role ARN 配置错误")
        print("  2. RAM 角色未正确授权")
        print("  3. 信任关系配置错误")
        print("  4. AccessKey 无权限")
        return None


def test_oss_credentials():
    """测试使用永久凭证访问 OSS"""
    print("\n=== 测试 4: 永久 AccessKey 访问 OSS ===")

    try:
        import oss2
        print(f"\n✅ OSS2 SDK 已安装")

        # 创建 OSS 客户端
        auth = oss2.Auth(
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET,
            settings.OSS_ENDPOINT.replace('https://', '').replace('http://', '')
        )

        bucket = oss2.Bucket(auth, settings.OSS_BUCKET)

        print(f"\n正在测试 OSS 连接...")
        print(f"  Bucket: {settings.OSS_BUCKET}")
        print(f"  Endpoint: {settings.OSS_ENDPOINT}")

        # 尝试列出 Bucket 信息
        bucket_info = bucket.get_bucket_info()
        print(f"\n✅ OSS 连接成功！")
        print(f"  Bucket Name: {bucket_info.name}")
        print(f"  Location: {bucket_info.location}")
        print(f"  Creation Date: {bucket_info.creation_date}")

        return True

    except Exception as e:
        print(f"\n❌ OSS 连接失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("阿里云 STS 连通性测试")
    print("=" * 60)

    # 测试 1: SDK 导入
    if not test_sts_import():
        print("\n❌ STS SDK 未正确安装，请运行:")
        print("   pip install aliyun-python-sdk-sts aliyun-python-sdk-core")
        return

    # 测试 2: 配置检查
    role_arn = test_sts_configuration()

    # 测试 3: STS 临时凭证
    credentials = test_sts_get_credentials()

    # 测试 4: OSS 永久凭证（备用方案）
    if not credentials:
        print("\n使用永久 AccessKey 测试 OSS 连接...")
        test_oss_credentials()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
