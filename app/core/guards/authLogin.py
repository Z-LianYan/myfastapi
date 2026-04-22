from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter,Query,HTTPException,Depends,Header

security = HTTPBearer()

def auth_guard(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    print('----',credentials)
    token = credentials.credentials  # 自动去掉 Bearer
    if token != "123456":
        raise HTTPException(401, "token 无效")
    return {"user_id": 1}