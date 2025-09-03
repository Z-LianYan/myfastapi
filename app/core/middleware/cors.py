from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def register_cors_middleware(app):
    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )