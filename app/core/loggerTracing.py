import sys
import uuid
import os
from contextvars import ContextVar

from fastapi import FastAPI, Request
from loguru import logger

# DEV = os.getenv("ENV") == "dev"

# =========================
# 1. 每个请求独立保存 trace_id
# =========================
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")


# =========================
# 2. Loguru 配置
# =========================
logger.remove()

def patch_record(record):
    """
    每次打日志时，自动把 trace_id 注入日志上下文
    """
    record["extra"]["trace_id"] = trace_id_var.get()
    return record

logger = logger.patch(patch_record)

logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "trace={extra[trace_id]} | "
        "{message}"
    )
)

logger.add(
    "logs/access/{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="00:00",# 每天 00:00 切新文件
    retention="30 days", # 日志文件保留时间
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | trace={extra[trace_id]} | {message}"
)

logger.add(
    "logs/error/{time:YYYY-MM-DD}.log",
    level="ERROR",
    rotation="00:00", # 每天 00:00 切新文件
    retention="90 days",# 日志文件保留时间
    encoding="utf-8",
    backtrace=True, # 显示完整异常调用链
    diagnose=True, # 报错时自动显示当时变量的值（超强） 注意： 生产环境要注意，可能泄露敏感信息，开发环境：True 生产环境：False
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | trace={extra[trace_id]} | {message}"
)

# print("dev===========",DEV, os.getenv("ENV"),os.environ)
# =========================
# 3. 注册 FastAPI 中间件
# =========================
def register_trace_middleware(app: FastAPI):
    print("==========loggerTracing.py")
    @app.middleware("http")
    async def trace_middleware(request: Request, call_next):
        print("==========loggerTracing.py---------")
        # 前端如果传了 trace_id 就沿用，没有就生成
        trace_id = request.headers.get("X-Trace-Id") or uuid.uuid4().hex[:16]

        # 放入上下文（当前请求专属）
        token = trace_id_var.set(trace_id)

        try:
            logger.info(f"{request.method} {request.url.path} request start")

            response = await call_next(request)

            logger.info(
                f"{request.method} {request.url.path} "
                f"status={response.status_code}==="
            )

            # 返回给前端，方便排查
            response.headers["X-Trace-Id"] = trace_id
            return response

        except Exception:
            logger.exception("Unhandled exception")
            raise

        finally:
            # 请求结束恢复上下文，避免串请求
            trace_id_var.reset(token)