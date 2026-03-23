"""
阿里云OSS客户端封装
"""
import os
import uuid
from datetime import datetime
from typing import Optional
from oss2 import Auth
from oss2 import Bucket
from oss2.exceptions import OssError

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class OSSClient:
    """阿里云OSS客户端单例类"""

    _instance: Optional["OSSClient"] = None
    _auth: Optional[Auth] = None
    _bucket: Optional[Bucket] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化OSS客户端（懒加载）"""
        self._auth = None
        self._bucket = None

    @property
    def auth(self) -> Auth:
        """获取OSS认证对象"""
        if self._auth is None:
            self._auth = Auth(
                settings.OSS_ACCESS_KEY_ID,
                settings.OSS_ACCESS_KEY_SECRET,
            )
            logger.info("OSS认证对象创建成功")
        return self._auth

    @property
    def bucket(self) -> Bucket:
        """获取OSS Bucket对象"""
        if self._bucket is None:
            # 使用oss2标准API: Bucket(auth, endpoint, bucket_name)
            # endpoint格式：oss-cn-shanghai.aliyuncs.com (不需要https://)
            self._bucket = Bucket(
                self.auth,
                settings.OSS_ENDPOINT,
                settings.OSS_BUCKET
            )
            logger.info(f"OSS Bucket对象创建成功: {settings.OSS_BUCKET}")
        return self._bucket

    def generate_filename(self, original_filename: str, prefix: str = "images") -> str:
        """
        生成唯一文件名

        Args:
            original_filename: 原始文件名
            prefix: 文件前缀

        Returns:
            唯一文件路径
        """
        # 获取文件扩展名
        ext = os.path.splitext(original_filename)[1]
        if not ext:
            ext = ".jpg"

        # 生成文件名: 前缀/年/月/时间戳_随机UUID.ext
        now = datetime.now()
        filename = f"{int(now.timestamp() * 1000)}_{uuid.uuid4().hex[:8]}{ext}"
        path = f"{prefix}/{now.year}/{now.month:02d}/{filename}"

        logger.debug(f"生成文件路径: {path}")
        return path

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        上传文件到OSS

        Args:
            file_content: 文件内容
            filename: 文件名
            content_type: Content-Type

        Returns:
            文件访问URL
        """
        try:
            # 上传文件
            self.bucket.put_object(
                filename,
                file_content,
                headers={
                    "Content-Type": content_type or "application/octet-stream",
                },
            )

            # 生成访问URL（使用自定义域名）
            file_url = f"{settings.OSS_HOST}/{filename}"

            logger.info(f"文件上传成功: {filename}")
            return file_url

        except OssError as e:
            logger.error(f"文件上传失败: {e}")
            raise

    def delete_file(self, filename: str) -> bool:
        """
        删除OSS文件

        Args:
            filename: 文件名

        Returns:
            是否删除成功
        """
        try:
            self.bucket.delete_object(filename)
            logger.info(f"文件删除成功: {filename}")
            return True

        except OssError as e:
            logger.error(f"文件删除失败: {e}")
            return False

    def file_exists(self, filename: str) -> bool:
        """
        检查文件是否存在

        Args:
            filename: 文件名

        Returns:
            文件是否存在
        """
        try:
            return self.bucket.object_exists(filename)
        except OssError:
            return False

    def get_file_url(self, filename: str) -> str:
        """
        获取文件访问URL

        Args:
            filename: 文件名

        Returns:
            文件URL（使用自定义域名）
        """
        return f"{settings.OSS_HOST}/{filename}"


# 创建全局实例
oss_client = OSSClient()


def get_oss_client() -> OSSClient:
    """
    获取OSS客户端实例

    Returns:
        OSS客户端单例
    """
    return oss_client
