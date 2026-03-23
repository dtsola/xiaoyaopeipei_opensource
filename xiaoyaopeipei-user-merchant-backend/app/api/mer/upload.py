"""
B端 - 文件上传接口（OSS 直传）
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.api.deps import get_db, get_current_merchant
from app.models.merchant import Merchant
from app.utils.response import success_response
from app.core.logger import get_logger
from app.core.exceptions import InvalidFileException, FileUploadException
from app.core.config import settings

router = APIRouter()
logger = get_logger(__name__)


# ==================== Schema定义 ====================

class OSSDirectUploadResponse(BaseModel):
    """OSS直传凭证响应（STS模式）"""
    region: str = Field(..., description="OSS区域")
    bucket: str = Field(..., description="OSS Bucket名称")
    accessKeyId: str = Field(..., description="STS临时AccessKey ID")
    accessKeySecret: str = Field(..., description="STS临时AccessKey Secret")
    stsToken: str = Field(..., description="STS安全令牌")
    endpoint: str = Field(default="", description="OSS endpoint（可选，使用region时为空）")
    host: str = Field(..., description="自定义域名（CDN加速域名）")
    dir: str = Field(..., description="上传目录前缀")
    expire: int = Field(..., description="过期时间（Unix时间戳）")


class OSSUploadCallbackRequest(BaseModel):
    """OSS上传回调请求"""
    key: str = Field(..., description="OSS文件路径")
    size: int = Field(..., description="文件大小")
    name: str = Field(..., description="原始文件名")
    etag: str = Field(default="", description="文件ETag")


# ==================== 接口实现 ====================

@router.get("/upload/oss/token")
async def get_oss_upload_token(
    current_merchant: Merchant = Depends(get_current_merchant),
):
    """
    获取OSS直传凭证

    返回前端OSS直传所需的配置信息
    前端使用 ali-oss SDK 直接上传文件到OSS

    安全说明：
    - 使用 STS 临时凭证，有效期1小时
    - 必须配置 OSS_STS_ROLE_ARN
    - 不支持永久 AccessKey 降级
    """
    logger.info(f"商家[{current_merchant.id}]获取OSS直传凭证")

    try:
        # 生成上传目录前缀
        now = datetime.now()
        upload_dir = f"peipei/merchant/{current_merchant.id}/images/{now.year}/{now.month:02d}"

        # 获取临时凭证（STS）
        from app.utils.sts import get_sts_client, STSNotAvailableError
        sts_client = get_sts_client()
        credentials = sts_client.get_temporary_credentials(
            role_session_name=f"merchant-{current_merchant.id}",
            duration_seconds=3600  # 1小时有效期
        )

        # 过期时间：1小时后
        expire_time = int((datetime.now() + timedelta(hours=1)).timestamp())

        return success_response(
            data=OSSDirectUploadResponse(
                region=settings.OSS_REGION,
                bucket=settings.OSS_BUCKET,
                accessKeyId=credentials["accessKeyId"],
                accessKeySecret=credentials["accessKeySecret"],
                stsToken=credentials["stsToken"],
                endpoint="",  # 使用 region 而不是 endpoint
                host=settings.OSS_HOST,
                dir=upload_dir,
                expire=expire_time,
            ).model_dump(),
            message="success",
        )

    except STSNotAvailableError as e:
        logger.error(f"STS 服务不可用: {e}")
        raise FileUploadException(message=f"STS 服务不可用，请检查配置：{str(e)}")
    except Exception as e:
        logger.error(f"获取OSS凭证失败: {e}")
        raise FileUploadException(message=f"获取上传凭证失败：{str(e)}")


@router.post("/upload/oss/callback")
async def oss_upload_callback(
    callback_data: OSSUploadCallbackRequest,
    current_merchant: Merchant = Depends(get_current_merchant),
):
    """
    OSS上传回调（可选）

    用于记录上传成功的文件信息
    """
    logger.info(f"OSS上传回调: merchant_id={current_merchant.id}, key={callback_data.key}")

    # 验证文件所有权
    merchant_prefix = "peipei/merchant/"
    if not callback_data.key.startswith(merchant_prefix):
        logger.warning(f"文件不属于该商家: key={callback_data.key}")
        raise InvalidFileException(message="文件所有权验证失败")

    # 生成文件访问URL
    file_url = f"{settings.OSS_HOST}/{callback_data.key}"

    return success_response(
        data={
            "url": file_url,
            "key": callback_data.key,
            "size": callback_data.size,
            "name": callback_data.name,
        },
        message="回调成功",
    )
