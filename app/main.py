from fastapi import FastAPI,Request,status
from app.routes import items

# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# import logging
# import traceback
from app.core.exceptions import register_exception_handlers

app = FastAPI(title="FastAPI Demo Project", version="1.0.0")

# 注册异常处理器
register_exception_handlers(app)

# 配置日志
# logging.basicConfig(level=logging.ERROR)
# logger = logging.getLogger(__name__)


# 注册路由
app.include_router(items.router, prefix="/api", tags=["项目"]) # tags 自动生成的 API 文档里分类显示

@app.get("/")
def root(name: str):
    return {"message": "Welcome to FastAPI Demo " + name}