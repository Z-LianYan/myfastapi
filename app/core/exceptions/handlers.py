from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException
import logging
import traceback

from app.utils.httpRes import success,fail


logger = logging.getLogger(__name__)

# 验证异常处理（参数验证）
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理参数验证异常"""
    logger.warning(f"参数验证失败: {exc.errors()}")

    # 提取第一个错误信息
    error_msg = "参数验证失败"
    if exc.errors():
        first_error = exc.errors()[0]
        error_msg = f"{first_error.get('msg')}"
        if 'loc' in first_error and len(first_error['loc']) > 1:
            field = first_error['loc'][-1]
            error_msg = f"Field '{field}' {error_msg}"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content= fail({
            "code": 422,
            "message": str(error_msg),
            "path": request.url.path,
        })
    )

# 处理 HTTP 异常
async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常"""
    logger.warning(f"HTTP异常: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content= fail({
            "code": exc.status_code,
            "message": exc.detail,
            "path": request.url.path,
        })
    )


# 全局异常处理
async def global_exception_handler(request: Request, exc: Exception):
    # 记录完整的错误堆栈
    logger.error(f"全局异常: {str(exc)}")
    logger.error(traceback.format_exc())
    # 根据异常类型返回不同的错误码
    if isinstance(exc, ValueError):
        status_code = status.HTTP_400_BAD_REQUEST
        message = str(exc)
    elif isinstance(exc, RequestValidationError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        message = "请求参数验证失败"
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "服务器内部错误"

    return JSONResponse(
        status_code = status_code,
        content = {
            "code": status_code,
            "message": message,
            "path": request.url.path,
        }
    )


def register_exception_handlers(app):
    """注册异常处理器到FastAPI应用"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    logger.info("异常处理器注册完成")