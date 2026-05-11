from sqlalchemy import text

from app.redis.redis import redis_manager
from app.db.session import engine

from app.core.loggerTracing import logger
from app.core.config import settings


async def startup():

    logger.info("系统开始启动")

    # ====================================
    # Redis
    # ====================================

    try:
        await redis_manager.connect()

        logger.info("Redis 连接成功")

    except Exception as e:
        logger.exception(
            "Redis 连接失败："
            f"{e}"
        )

    # ====================================
    # MySQL
    # ====================================

    try:

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        logger.info(
            "MySQL 连接成功:"
            f"{settings.DATABASE_URL if settings.ENV == 'dev' else '***hidden***'}"
        )
    except Exception as e:
        # 关闭当前数据库会话：这里没有关闭mysql 数据库会话，因为不是长链接（单个连接），是连接池管理器， 在get_db() 已经做了 ，
        # with engine.connect() as conn: 离开 with 时：conn 自动关闭 了
        logger.exception(
            "MySQL 连接失败："
            f"{settings.DATABASE_URL if settings.ENV == 'dev' else '***hidden***'}"
            f"{e}"
        )

    logger.info("系统启动完成")