from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter,Query,HTTPException,Depends,Header
from  app.utils.joseJwt import verify_access_token
security = HTTPBearer()

# def auth_guard(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ):
#     print('----',credentials)
#     token = credentials.credentials  # 自动去掉 Bearer
#
#     if token != "123456":
#         raise HTTPException(400, "token 无效")
#     return {"user_id": 1}


def login_auth_guard(
    accesstoken: str = Header(None)
):
    print('login_auth_guard----token', accesstoken)
    # try:
    #     res = verify_access_token(accessToken)
    #     return res
    # except Exception as e:
    #     raise HTTPException(400, f"令牌无效{e}")



