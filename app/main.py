from fastapi import FastAPI,Request,status
from app.routes import items
from app.core.exceptions import register_exception_handlers
from app.core.middleware import logging_middleware,auth_middleware,timing_middleware,register_cors_middleware

app = FastAPI(title="FastAPI Demo Project", version="1.0.0")

# 注册异常处理器
register_exception_handlers(app)

# 注册中间件
register_cors_middleware(app)
# 添加中间件
app.middleware("http")(timing_middleware)
app.middleware("http")(logging_middleware)
app.middleware("http")(auth_middleware)


# 注册路由
app.include_router(items.router, prefix="/api", tags=["项目"]) # tags 自动生成的 API 文档里分类显示

@app.get("/")
def root(name: str):
    return {"message": "Welcome to FastAPI Demo " + name}