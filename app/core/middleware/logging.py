# import logging
from fastapi import Request
# from app.core.logger import logger
# logger = logging.getLogger(__name__)
from app.core.loggerTracing import logger, register_trace_middleware


async def logging_middleware(request: Request, call_next):
    print("print====logging_middleware===>",__name__)
    """日志记录中间件"""
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Client: {request.client.host if request.client else 'unknown'}")
    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")
    return response