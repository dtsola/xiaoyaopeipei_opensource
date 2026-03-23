"""
图片处理工具
"""
import io
from typing import Optional, Tuple
from PIL import Image
from PIL import ImageEnhance

from app.core.logger import get_logger

logger = get_logger(__name__)


# 图片格式常量
ALLOWED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_SIZE = 1920  # 长边最大尺寸
JPEG_QUALITY = 85  # JPEG压缩质量


class ImageProcessor:
    """图片处理器"""

    @staticmethod
    def compress_image(
        image_data: bytes,
        max_size: int = MAX_IMAGE_SIZE,
        quality: int = JPEG_QUALITY,
        output_format: str = "JPEG",
    ) -> bytes:
        """
        压缩图片

        Args:
            image_data: 图片二进制数据
            max_size: 长边最大尺寸
            quality: 压缩质量（1-100）
            output_format: 输出格式（JPEG/PNG/WebP）

        Returns:
            压缩后的图片二进制数据
        """
        try:
            # 打开图片
            image = Image.open(io.BytesIO(image_data))

            # 转换RGB模式（用于JPEG输出）
            if output_format.upper() in ["JPEG", "JPG"]:
                if image.mode in ["RGBA", "LA", "P"]:
                    # 创建白色背景
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    if image.mode == "P":
                        image = image.convert("RGBA")
                    background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
                    image = background
                elif image.mode != "RGB":
                    image = image.convert("RGB")
            elif output_format.upper() == "PNG" and image.mode not in ["RGB", "RGBA"]:
                image = image.convert("RGBA")

            # 计算缩放比例
            width, height = image.size
            if max(width, height) > max_size:
                if width > height:
                    new_width = max_size
                    new_height = int(height * (max_size / width))
                else:
                    new_height = max_size
                    new_width = int(width * (max_size / height))

                image = image.resize((new_width, new_height), Image.LANCZOS)

            # 保存到内存
            output = io.BytesIO()

            if output_format.upper() in ["JPEG", "JPG"]:
                image.save(output, format="JPEG", quality=quality, optimize=True)
            elif output_format.upper() == "PNG":
                image.save(output, format="PNG", optimize=True)
            elif output_format.upper() == "WEBP":
                image.save(output, format="WebP", quality=quality, method=6)
            else:
                raise ValueError(f"不支持的输出格式: {output_format}")

            output.seek(0)
            compressed_data = output.read()

            logger.info(f"图片压缩成功: 原始大小={len(image_data)}字节, 压缩后={len(compressed_data)}字节")

            return compressed_data

        except Exception as e:
            logger.error(f"图片压缩失败: {e}")
            raise

    @staticmethod
    def get_image_info(image_data: bytes) -> dict:
        """
        获取图片信息

        Args:
            image_data: 图片二进制数据

        Returns:
            图片信息字典
        """
        try:
            image = Image.open(io.BytesIO(image_data))

            return {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
            }

        except Exception as e:
            logger.error(f"获取图片信息失败: {e}")
            raise

    @staticmethod
    def validate_image_type(filename: str) -> bool:
        """
        验证图片文件类型

        Args:
            filename: 文件名

        Returns:
            是否为允许的图片格式
        """
        ext = "." + filename.split(".")[-1].lower() if "." in filename else ""
        return ext in ALLOWED_IMAGE_FORMATS

    @staticmethod
    def resize_image(
        image_data: bytes,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
    ) -> bytes:
        """
        调整图片尺寸

        Args:
            image_data: 图片二进制数据
            width: 目标宽度
            height: 目标高度
            maintain_aspect: 是否保持宽高比

        Returns:
            调整后的图片二进制数据
        """
        try:
            image = Image.open(io.BytesIO(image_data))

            # 计算新尺寸
            if width and height:
                if maintain_aspect:
                    # 保持宽高比
                    img_width, img_height = image.size
                    aspect_ratio = img_width / img_height

                    if (width / height) > aspect_ratio:
                        new_width = width
                        new_height = int(width / aspect_ratio)
                    else:
                        new_height = height
                        new_width = int(height * aspect_ratio)
                else:
                    new_width, new_height = width, height

                image = image.resize((new_width, new_height), Image.LANCZOS)

            # 保存到内存
            output = io.BytesIO()
            image.save(output, format="PNG")
            output.seek(0)

            return output.read()

        except Exception as e:
            logger.error(f"调整图片尺寸失败: {e}")
            raise

    @staticmethod
    def create_thumbnail(
        image_data: bytes,
        size: Tuple[int, int] = (200, 200),
    ) -> bytes:
        """
        创建缩略图

        Args:
            image_data: 图片二进制数据
            size: 缩略图尺寸

        Returns:
            缩略图的二进制数据
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(size, Image.LANCZOS)

            # 转换为RGB（如果是RGBA且有透明背景）
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background

            output = io.BytesIO()
            image.save(output, format="JPEG", quality=80)
            output.seek(0)

            return output.read()

        except Exception as e:
            logger.error(f"创建缩略图失败: {e}")
            raise


# 创建全局实例
image_processor = ImageProcessor()


def get_image_processor() -> ImageProcessor:
    """
    获取图片处理器实例

    Returns:
        图片处理器单例
    """
    return image_processor
