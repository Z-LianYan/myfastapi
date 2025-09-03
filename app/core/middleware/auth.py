from fastapi import Request, status, HTTPException
async def auth_middleware(request: Request, call_next):
    print("print====auth_middleware===>")
    """认证中间件"""
    # 跳过某些路径的认证
    if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health"]:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")

    # if not auth_header or not auth_header.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    # token = auth_header.replace("Bearer ", "")
    # # 这里可以添加实际的token验证逻辑
    # if token != "secret-token":
    #     raise HTTPException(status_code=401, detail="Invalid token")
    #
    # # 将用户信息添加到请求状态中
    # request.state.user = {"id": 1, "username": "test_user"}

    return await call_next(request)