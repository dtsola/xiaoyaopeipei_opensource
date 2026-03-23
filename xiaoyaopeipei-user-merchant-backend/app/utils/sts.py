"""
阿里云 STS 临时凭证服务

用于生成临时的 OSS 访问凭证，提高安全性

注意：
1. 必须安装 aliyun-python-sdk-sts 和 aliyun-python-sdk-core
2. 必须配置 OSS_STS_ROLE_ARN
3. 不支持降级使用永久 AccessKey
"""
import json
from typing import Optional

from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

# 导入 STS SDK
try:
    from aliyunsdkcore.client import AcsClient
    from aliyunsdksts.request.v20150401 import AssumeRoleRequest
    from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
    _STS_EXCEPTIONS = (ServerException, ClientException)
    logger.info("STS SDK 已加载")
except ImportError as e:
    logger.error(f"STS SDK 导入失败: {e}")
    raise RuntimeError(
        "STS SDK 未安装，请运行: pip install aliyun-python-sdk-sts aliyun-python-sdk-core"
    )


class STSNotAvailableError(Exception):
    """STS 不可用异常"""
    pass


class STSClient:
    """STS 客户端"""

    def __init__(self):
        """初始化 STS 客户端"""
        self.role_arn: Optional[str] = getattr(settings, 'OSS_STS_ROLE_ARN', None)

        if not self.role_arn:
            raise STSNotAvailableError("未配置 OSS_STS_ROLE_ARN，无法使用 STS 临时凭证")

        self.client = AcsClient(
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET,
            settings.OSS_REGION
        )

    def get_temporary_credentials(
        self,
        role_session_name: str = "merchant-upload",
        duration_seconds: int = 3600
    ) -> dict:
        """
        获取临时访问凭证

        Args:
            role_session_name: 会话名称
            duration_seconds: 有效期（秒），最大 3600

        Returns:
            包含临时凭证的字典

        Raises:
            STSNotAvailableError: STS 不可用时抛出
        """
        try:
            # 创建并执行 AssumeRole 请求
            request = AssumeRoleRequest.AssumeRoleRequest()
            request.set_RoleArn(self.role_arn)
            request.set_RoleSessionName(role_session_name)
            request.set_DurationSeconds(duration_seconds)

            response = self.client.do_action_with_exception(request)
            result = json.loads(response.decode('utf-8'))
            credentials = result['Credentials']

            logger.info(f"成功获取 STS 临时凭证，过期时间: {credentials['Expiration']}")

            return {
                "accessKeyId": credentials['AccessKeyId'],
                "accessKeySecret": credentials['AccessKeySecret'],
                "stsToken": credentials['SecurityToken'],
                "expiration": credentials['Expiration']
            }

        except _STS_EXCEPTIONS as e:
            logger.error(f"STS API 调用失败: {e}")
            raise STSNotAvailableError(f"STS API 调用失败: {e}")
        except Exception as e:
            logger.error(f"获取临时凭证失败: {e}")
            raise STSNotAvailableError(f"获取临时凭证失败: {e}")


# 全局单例
sts_client = STSClient()


def get_sts_client() -> STSClient:
    """获取 STS 客户端实例"""
    return sts_client
