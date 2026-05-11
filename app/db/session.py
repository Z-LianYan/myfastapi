from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os
DEV = os.getenv("ENV") == "dev"
print("mysql_url",settings.DATABASE_URL)
# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,

    # 开发环境打印 SQL
    echo=settings.DEBUG,

    # 自动检测失效连接
    pool_pre_ping=True,

    # 连接池
    pool_size=10,
    max_overflow=20
)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("MySQL 连接成功",settings.DATABASE_URL)

except Exception as e:
    print("MySQL 连接失败",settings.DATABASE_URL)
    print(e)



# 创建 Session 工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)