"""
安全相关模块
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==================== AES加密 ====================

def _get_fernet_key() -> bytes:
    """
    生成Fernet密钥

    使用AES_KEY的前32字节作为密钥
    """
    # 确保密钥长度为32字节（Fernet要求）
    key = settings.AES_KEY[:32].encode()
    # Base64编码以符合Fernet要求
    return base64.urlsafe_b64encode(key.ljust(32, b'0'))


# 创建Fernet实例
_fernet: Optional[Fernet] = None

def _get_fernet() -> Fernet:
    """获取Fernet实例（懒加载）"""
    global _fernet
    if _fernet is None:
        try:
            key = _get_fernet_key()
            _fernet = Fernet(key)
            logger.info("AES加密初始化成功")
        except Exception as e:
            logger.error(f"AES加密初始化失败: {e}")
            raise
    return _fernet


def encrypt_data(plain_text: str) -> str:
    """
    加密数据（用于手机号、微信号等敏感信息）

    Args:
        plain_text: 明文

    Returns:
        加密后的Base64字符串
    """
    try:
        fernet = _get_fernet()
        encrypted = fernet.encrypt(plain_text.encode('utf-8'))
        return encrypted.decode('utf-8')
    except Exception as e:
        logger.error(f"数据加密失败: {e}")
        raise


def decrypt_data(encrypted_text: str) -> str:
    """
    解密数据

    Args:
        encrypted_text: 加密的Base64字符串

    Returns:
        明文
    """
    try:
        fernet = _get_fernet()
        decrypted = fernet.decrypt(encrypted_text.encode('utf-8'))
        return decrypted.decode('utf-8')
    except Exception as e:
        logger.error(f"数据解密失败: {e}")
        return ""


def mask_phone(phone: str) -> str:
    """
    手机号脱敏显示

    Args:
        phone: 手机号（明文或加密）

    Returns:
        脱敏后的手机号（如：138****5678）
    """
    # 尝试解密
    try:
        decrypted = decrypt_data(phone)
        phone_number = decrypted
    except:
        phone_number = phone

    # 脱敏处理
    if len(phone_number) == 11 and phone_number.isdigit():
        return f"{phone_number[:3]}****{phone_number[7:]}"
    return phone_number


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT Token

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        JWT Token字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    验证JWT Token

    Args:
        token: JWT Token字符串

    Returns:
        解码后的数据，验证失败返回None
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def hash_password(password: str) -> str:
    """
    密码哈希

    Args:
        password: 明文密码

    Returns:
        哈希后的密码
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码

    Returns:
        是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)
