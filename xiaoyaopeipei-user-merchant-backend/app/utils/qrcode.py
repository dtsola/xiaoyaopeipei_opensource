"""
二维码生成工具
"""
import io
import qrcode
from typing import Optional
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SquareGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer

from app.core.config import settings
from app.core.logger import get_logger
from app.utils.oss import get_oss_client

logger = get_logger(__name__)


# ==================== 配置常量 ====================

# 二维码配置
QR_SIZE = 256  # 二维码尺寸（像素）
QR_VERSION = 1  # QR码版本（1-40，数字越大存储容量越大）
QR_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_M  # 纠错级别（L/M/Q/H）
QR_BORDER = 4  # 边框大小


class QRCodeGenerator:
    """二维码生成器"""

    def __init__(self):
        self.oss_client = get_oss_client()

    def generate_qrcode_image(
        self,
        data: str,
        size: int = QR_SIZE,
        fill_color: str = "000000",
        back_color: str = "FFFFFF",
        style: Optional[str] = None,
    ) -> bytes:
        """
        生成二维码图片

        Args:
            data: 二维码内容（URL）
            size: 图片尺寸
            fill_color: 前景色（十六进制）
            back_color: 背景色（十六进制）
            style: 样式（simple/rounded）

        Returns:
            PNG图片二进制数据
        """
        try:
            # 创建QR码实例
            qr = qrcode.QRCode(
                version=QR_VERSION,
                error_correction=QR_ERROR_CORRECTION,
                box_size=10,
                border=QR_BORDER,
            )

            # 添加数据
            qr.add_data(data)
            qr.make(fit=True)

            # 创建图片
            if style == "rounded":
                img = qr.make_image(
                    fill_color=f"#{fill_color}",
                    back_color=f"#{back_color}",
                    image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                )
            else:
                # 默认方形
                img = qr.make_image(
                    fill_color=f"#{fill_color}",
                    back_color=f"#{back_color}",
                )

            # 调整尺寸
            if img.size != (size, size):
                img = img.resize((size, size))

            # 转换为PNG字节流
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            logger.info(f"二维码生成成功: data={data[:50]}...")
            return buffer.read()

        except Exception as e:
            logger.error(f"二维码生成失败: {e}")
            raise

    def generate_merchant_qrcode(
        self,
        merchant_id: int,
        share_link: str,
        style: str = "simple",
    ) -> str:
        """
        生成商家专属二维码

        Args:
            merchant_id: 商家ID
            share_link: 完整分享链接（如 https://peipei.xiaoyaos.com/?shop=shop_123）
            style: 样式（simple/rounded）

        Returns:
            二维码OSS URL
        """
        # 直接使用传入的完整分享链接
        share_url = share_link

        # 生成二维码图片
        image_data = self.generate_qrcode_image(
            data=share_url,
            style=style,
        )

        # 生成文件名
        filename = self.oss_client.generate_filename(
            original_filename=f"merchant_{merchant_id}_qrcode.png",
            prefix=f"peipei/merchant/{merchant_id}/qrcode",
        )

        # 上传到OSS
        qrcode_url = self.oss_client.upload_file(
            file_content=image_data,
            filename=filename,
            content_type="image/png",
        )

        logger.info(f"商家二维码已生成并上传: merchant_id={merchant_id}, url={qrcode_url}")
        return qrcode_url

    def generate_shop_qrcode_if_not_exists(
        self,
        merchant_id: int,
        share_link: str,
        current_qrcode_url: Optional[str],
    ) -> str:
        """
        生成商家二维码（如果不存在）

        Args:
            merchant_id: 商家ID
            share_link: 分享链接
            current_qrcode_url: 当前二维码URL

        Returns:
            二维码URL
        """
        # 如果已有二维码，直接返回
        if current_qrcode_url:
            return current_qrcode_url

        # 生成新二维码
        return self.generate_merchant_qrcode(
            merchant_id=merchant_id,
            share_link=share_link,
        )


# 创建全局实例
qrcode_generator = QRCodeGenerator()


def get_qrcode_generator() -> QRCodeGenerator:
    """
    获取二维码生成器实例

    Returns:
        二维码生成器单例
    """
    return qrcode_generator
