from fastapi import FastAPI
from app.routes import items

app = FastAPI(title="FastAPI Demo Project", version="1.0.0")

# 注册路由
app.include_router(items.router, prefix="/api", tags=["项目"]) # tags 自动生成的 API 文档里分类显示

@app.get("/")
def root(name: str):
    return {"message": "Welcome to FastAPI Demo " + name}