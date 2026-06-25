from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter,Query,HTTPException,Depends,Header

from app.models.admin import AdminLoginParams
from  app.utils.joseJwt import verify_access_token
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models.admin import Admin
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
    accessToken: str = Header(None),
    db: Session = Depends(get_db),
):
    print('login_auth_guard----token', accessToken)
    try:
        res = verify_access_token(accessToken)
        if not res or not res.get('id') or not res.get('exp'):
            raise HTTPException(400,"令牌无效！")

        now = datetime.now().timestamp()
        if now > res.get('exp'):
            raise HTTPException(400,"令牌已失效")

        admin = db.query(Admin).filter(
            Admin.id==res.get('id'),
            Admin.delete_time.is_(None),
        ).first()
        if not admin:
            raise HTTPException(400,"令牌无效！！")
        return admin
    except Exception as e:
        raise HTTPException(getattr(e, "status_code", 400), f"{getattr(e, "detail", str(e))}")



