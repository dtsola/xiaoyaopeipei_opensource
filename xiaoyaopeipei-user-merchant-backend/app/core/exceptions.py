"""
自定义异常类
定义应用中使用的所有自定义异常
"""
from typing import Optional, Any


class AppException(Exception):
    """应用基础异常类"""

    def __init__(
        self,
        message: str,
        code: int = 500,
        data: Optional[Any] = None,
    ):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)


class BadRequestException(AppException):
    """错误请求异常 (400)"""

    def __init__(self, message: str = "错误的请求", data: Optional[Any] = None):
        super().__init__(message=message, code=400, data=data)


class UnauthorizedException(AppException):
    """未授权异常 (401)"""

    def __init__(self, message: str = "未授权，请先登录", data: Optional[Any] = None):
        super().__init__(message=message, code=401, data=data)


class ForbiddenException(AppException):
    """禁止访问异常 (403)"""

    def __init__(self, message: str = "没有权限访问", data: Optional[Any] = None):
        super().__init__(message=message, code=403, data=data)


class NotFoundException(AppException):
    """资源不存在异常 (404)"""

    def __init__(self, message: str = "资源不存在", data: Optional[Any] = None):
        super().__init__(message=message, code=404, data=data)


class ConflictException(AppException):
    """冲突异常 (409)"""

    def __init__(self, message: str = "资源冲突", data: Optional[Any] = None):
        super().__init__(message=message, code=409, data=data)


class ValidationException(AppException):
    """验证失败异常 (422)"""

    def __init__(self, message: str = "数据验证失败", data: Optional[Any] = None):
        super().__init__(message=message, code=422, data=data)


class TooManyRequestsException(AppException):
    """请求过多异常 (429)"""

    def __init__(self, message: str = "请求过于频繁，请稍后再试", data: Optional[Any] = None):
        super().__init__(message=message, code=429, data=data)


class InternalServerException(AppException):
    """服务器内部错误异常 (500)"""

    def __init__(self, message: str = "服务器内部错误", data: Optional[Any] = None):
        super().__init__(message=message, code=500, data=data)


class ServiceUnavailableException(AppException):
    """服务不可用异常 (503)"""

    def __init__(self, message: str = "服务暂时不可用", data: Optional[Any] = None):
        super().__init__(message=message, code=503, data=data)


# ==================== 业务异常 ====================

class MerchantNotFoundException(NotFoundException):
    """商家不存在异常"""

    def __init__(self, message: str = "商家不存在"):
        super().__init__(message=message)


class MerchantExistsException(ConflictException):
    """商家已存在异常"""

    def __init__(self, message: str = "商家已存在"):
        super().__init__(message=message)


class InvalidCredentialsException(UnauthorizedException):
    """无效凭证异常"""

    def __init__(self, message: str = "用户名或密码错误"):
        super().__init__(message=message)


class TokenExpiredException(UnauthorizedException):
    """Token过期异常"""

    def __init__(self, message: str = "Token已过期，请重新登录"):
        super().__init__(message=message)


class SKUNotFoundException(NotFoundException):
    """SKU不存在异常"""

    def __init__(self, message: str = "配置不存在"):
        super().__init__(message=message)


class ConversationNotFoundException(NotFoundException):
    """对话不存在异常"""

    def __init__(self, message: str = "对话不存在"):
        super().__init__(message=message)


class LeadNotFoundException(NotFoundException):
    """线索不存在异常"""

    def __init__(self, message: str = "线索不存在"):
        super().__init__(message=message)


class AIServiceException(InternalServerException):
    """AI服务异常"""

    def __init__(self, message: str = "AI服务暂时不可用"):
        super().__init__(message=message)


class FileUploadException(BadRequestException):
    """文件上传异常"""

    def __init__(self, message: str = "文件上传失败"):
        super().__init__(message=message)


class InvalidFileException(BadRequestException):
    """无效文件异常"""

    def __init__(self, message: str = "无效的文件类型或大小"):
        super().__init__(message=message)


class MembershipExpiredException(ForbiddenException):
    """会员已过期异常"""

    def __init__(
        self,
        message: str = "会员已过期，请联系客服续期",
        data: Optional[Any] = None
    ):
        # 默认提供联系信息
        default_data = {
            "contact_wechat": "dtsola",
            "contact_name": "小遥配配客服",
            "message": "请添加微信客服咨询续费事宜"
        }
        if data:
            default_data.update(data)
        super().__init__(message=message, data=default_data)
