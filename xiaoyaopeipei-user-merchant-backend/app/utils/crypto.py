"""
加密解密工具
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from app.core.config import settings


def encrypt_aes(plaintext: str) -> str:
    """
    AES加密

    Args:
        plaintext: 明文

    Returns:
        密文（Base64编码）
    """
    key = settings.AES_KEY[:32].encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    iv = cipher.iv
    return b64encode(iv + ct_bytes).decode("utf-8")


def decrypt_aes(ciphertext: str) -> str:
    """
    AES解密

    Args:
        ciphertext: 密文（Base64编码）

    Returns:
        明文
    """
    key = settings.AES_KEY[:32].encode("utf-8")
    data = b64decode(ciphertext)
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode("utf-8")
