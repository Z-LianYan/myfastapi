from app.redis.redis import redis_manager

from app.core.loggerTracing import logger
from app.db.session import engine

async def shutdown():

    logger.info("<app.core.shutdown.py> 系统开始关闭")

    # ====================================
    # 关闭 Redis
    # ====================================

    try:

        await redis_manager.close()

        logger.info("<app.core.shutdown.py> Redis已关闭")

    except Exception as e:
        logger.exception(
            "<app.core.shutdown.py> Redis关闭失败："
            f"{e}"
        )



    # ====================================
    # MySQL
    # ====================================
    try:

        engine.dispose() # 关闭连接池 释放所有连接

        logger.info("<app.core.shutdown.py> MySQL连接池已关闭")

    except Exception as e:
        logger.exception(
            "<app.core.shutdown.py> 关闭MYSQL连接池失败："
            f"{e}"
        )


    logger.info("系统关闭完成")