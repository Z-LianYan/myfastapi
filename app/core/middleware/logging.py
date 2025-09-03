import logging
from fastapi import Request

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next):
    print("print====logging_middleware===>")
    """日志记录中间件"""
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Client: {request.client.host if request.client else 'unknown'}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")
    return response