import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# ==========================================
# 获取当前运行环境
# 没设置 ENV 时，默认 dev
# ==========================================
ENV = os.getenv("ENV", "dev")


class Settings(BaseSettings):
    """
    项目所有配置统一放这里
    """

    # ==========================================
    # 基础配置
    # ==========================================
    ENV: str = ENV                     # 当前环境
    APP_NAME: str = "My FastAPI API"  # 项目名称
    DEBUG: bool = True                # 是否调试模式

    # ==========================================
    # 数据库配置
    # ==========================================
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "test"

    # ==========================================
    # Redis 配置
    # ==========================================
    REDIS_HOST: str = "106.53.161.135"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "julian888666"

    # ==========================================
    # JWT 配置
    # ==========================================
    JWT_SECRET: str = "change_me"
    JWT_EXPIRE_MINUTES: int = 1440

    # ==========================================
    # Swagger 文档配置
    # ==========================================
    ENABLE_DOCS: bool = False

    # ==========================================
    # 自动读取对应环境文件，会覆盖以上存在的变量
    # 例如：
    # ENV=dev  -> .env.dev
    # ENV=prod -> .env.prod
    # ==========================================
    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # ==========================================
    # 拼接数据库连接地址
    # ==========================================
    @property
    def DATABASE_URL(self):
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def REDIS_URL0(self):
        return (
            f"redis://:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        )

    @property
    def REDIS_URL1(self):
        return (
            f"redis://:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}/1"
        )


# ==========================================
# lru_cache 缓存函数结果，避免重复创建对象。
# 单例模式（只创建一次）
# 避免每次 import 都重新读取配置
# ==========================================
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()