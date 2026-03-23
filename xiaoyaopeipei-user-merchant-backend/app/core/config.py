"""
应用配置文件
支持多环境配置：通过设置 APP_ENV 环境变量切换
- development: 开发环境（默认），读取 .env.development
- production: 生产环境，读取 .env.production
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """应用配置"""

    # ==================== 应用配置 ====================
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001

    # ==================== 数据库配置 ====================
    DATABASE_URL: str = "mysql+pymysql://root:root123@localhost:3306/xiaoyao?charset=utf8mb4"

    # ==================== JWT配置 ====================
    JWT_SECRET: str = "your_jwt_secret_key_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080  # 7天

    # ==================== 通义千问配置 ====================
    QWEN_API_KEY: str = "sk-xxxxxxxxxxxxxxxx"
    QWEN_MODEL: str = "qwen-plus"
    QWEN_TEMPERATURE: float = 0.7
    QWEN_MAX_TOKENS: int = 2000

    # ==================== 阿里云OSS配置 ====================
    OSS_ACCESS_KEY_ID: str = ""
    OSS_ACCESS_KEY_SECRET: str = ""
    OSS_BUCKET: str = ""
    OSS_ENDPOINT: str = "oss-cn-hangzhou.aliyuncs.com"
    OSS_REGION: str = "cn-hangzhou"
    OSS_HOST: str = "https://file.xiaoyaosai.com"  # OSS自定义域名
    # STS 角色配置（用于生成临时凭证，提高安全性）
    # 格式: acs:ram::<主账号ID>:role/<角色名>
    # 示例: acs:ram::1234567890123456:role/oss-upload-role
    OSS_STS_ROLE_ARN: str = ""  # 留空则使用永久 AccessKey（不推荐）

    # ==================== 缓存配置 ====================
    CACHE_MAX_SIZE: int = 1000
    CACHE_TTL: int = 3600

    # ==================== 加密配置 ====================
    AES_KEY: str = "your_aes_key_32_characters_long"

    # ==================== 日志配置（Loguru） ====================
    LOG_LEVEL: str = "INFO"
    LOG_ROTATION: str = "00:00"
    LOG_RETENTION: str = "30 days"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # ==================== 前端URL配置 ====================
    # C端（用户端）前端地址
    USER_FRONTEND_URL: str = "http://localhost:5173"  # 开发环境默认值
    # 生产环境：https://peipei.xiaoyaos.com
    USER_FRONTEND_URL_PROD: str = "https://peipei.xiaoyaos.com"

    # ==================== 会员配置 ====================
    # 会员默认天数（注册时赠送）
    MEMBERSHIP_DEFAULT_DAYS: int = 7
    # 会员续期提醒阈值（天）
    MEMBERSHIP_RENEWAL_THRESHOLD: int = 3

    # ==================== CORS配置 ====================
    # CORS允许的域名（生产环境需要配置具体域名）
    CORS_ORIGINS: list = [
        "http://localhost:5173",  # C端本地开发
        "http://localhost:5174",  # B端本地开发
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    # 生产环境域名（需要在部署时配置）
    CORS_ORIGINS_PROD: list = [
        "https://peipei.xiaoyaos.com",   # C端生产环境
        "https://peipei-mer.xiaoyaos.com",  # B端生产环境
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: list = ["*"]


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（单例模式）

    支持通过 APP_ENV 环境变量切换配置文件：
    - development: 使用 .env.development（默认）
    - production: 使用 .env.production
    """
    app_env = os.getenv("APP_ENV", "development")

    # 根据环境选择对应的 .env 文件
    env_file_map = {
        "development": ".env.development",
        "test": ".env.test",
        "production": ".env.production",
    }
    env_file = env_file_map.get(app_env, ".env.development")

    return Settings(_env_file=env_file, _env_file_encoding="utf-8")


# 导出配置实例
settings = get_settings()
