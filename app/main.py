from fastapi import FastAPI
from app.routes import items,admin
from app.core.exceptions import register_exception_handlers
from app.core.middleware import logging_middleware,auth_middleware,timing_middleware,register_cors_middleware
from app.core.loggerTracing import register_trace_middleware
from app.redis.redis import redis_manager
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.startup import startup
from  app.core.shutdown import shutdown

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动
    await startup()

    # yield 前 应用启动时执行
    yield
    # yield 后 应用关闭时执行

    # 关闭
    await shutdown()


app = FastAPI(
    title="FastAPI Demo Project",
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url=None,
    version="1.0.0",
    lifespan=lifespan
)



# 注册异常处理器
register_exception_handlers(app)

# 注册中间件
register_cors_middleware(app)

'''
注册 HTTP middleware
“洋葱模型”越靠后越先执行
'''
app.middleware("http")(logging_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(timing_middleware)
register_trace_middleware(app) # 链式追踪日记


# 注册路由
app.include_router(items.router, prefix="/api", tags=["项目"]) # tags 自动生成的 API 文档里分类显示
app.include_router(admin.router, prefix="/api/v1/admin", tags=["管理员"]) # tags 自动生成的 API 文档里分类显示

@app.get("/")
def root(name: str):
    return {"message": "Welcome to FastAPI Demo " + name}


# 导入所有模型
from app.db.models.init import *
from app.db.base import Base
# print(Base.metadata.tables)
from app.db.session import engine
# 自动创建表
Base.metadata.create_all(bind=engine)