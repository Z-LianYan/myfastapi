import time
from fastapi import Request


async def timing_middleware(request: Request, call_next):
    print("timing_middleware===>>")
    """处理时间中间件"""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time-MS"] = str(round(process_time * 1000, 2))

    return response