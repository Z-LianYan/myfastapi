from fastapi import APIRouter, Query, HTTPException, Depends, Header, Request, Response

from app.utils.httpRes import success, fail, ResStructure
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.guards.authLogin import login_auth_guard
from jose import jwt

router = APIRouter()
# def create_item(user=Depends(login_auth_guard)):
@router.post("/login", response_model=ResStructure)
def create_item():
    jwt_secret = "julian!&&&kkkk"
    print('accessionToken==>>', "user")
    token = jwt.encode(
        {"a":"to_encode"},
        jwt_secret, # 密钥
        algorithm="HS256" # 加密算法
    )
    return success({
        "code": 200,
        "data": token,
        "message": "操作成功"
    })