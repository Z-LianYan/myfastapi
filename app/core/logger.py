import os
import sys
from loguru import logger

LOG_DIR = "logs"

os.makedirs(f"{LOG_DIR}/access", exist_ok=True)
os.makedirs(f"{LOG_DIR}/error", exist_ok=True)
os.makedirs(f"{LOG_DIR}/audit", exist_ok=True)

# 删除默认配置
logger.remove()

# 控制台输出（彩色）
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "{message}"
)

# 访问日志（每天一个文件）
logger.add(
    "logs/access/{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="00:00", # 每天 00:00 切新文件
    retention="30 days", # 日志文件保留时间
    encoding="utf-8"
)

# 错误日志
logger.add(
    "logs/error/{time:YYYY-MM-DD}.log",
    level="ERROR",
    rotation="00:00",
    retention="90 days",
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)

# 审计日志（退款、删除订单等）
# logger.add(
#     "logs/audit/{time:YYYY-MM-DD}.log",
#     level="INFO",
#     filter=lambda record: record["extra"].get("audit") is True,
#     rotation="00:00",
#     retention="180 days",
#     encoding="utf-8"
# )

# 审计日志 使用方式
# logger.bind(audit=True).info(
#     "操作员1001 删除订单888"
# )