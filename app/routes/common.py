import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException,Request

from app.db.models import AdminRole,Menu
from app.utils.httpRes import ResStructure
from app.utils.httpRes import success,fail
from app.models.menu import GetMeneList, AddMenu, EditMenu, DelMenu


from sqlalchemy import func,or_,and_,text
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.guards.authLogin import login_auth_guard
router = APIRouter()
import json



# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/getQiNiuToken",description="获取资源上传七牛云token",summary="获取资源上传七牛云token", response_model = ResStructure)
async def get_list(
    db: Session = Depends(get_db),
    # admin=Depends(login_auth_guard),
):
    try:


        return success({
            "data": {
                "upload_token": "2J175TblvDTRqVcw_Uajw0VjyxTpfxeEz6vljRTZ:waR6T-tjxJWQbLDXtj0yTriXv8Y=:eyJzY29wZSI6InN0YXRpY2RldiIsInJldHVybkJvZHkiOiJ7XCJrZXlcIjpcIiQoa2V5KVwiLFwiaGFzaFwiOlwiJChldGFnKVwiLFwiZnNpemVcIjokKGZzaXplKSxcImJ1Y2tldFwiOlwiJChidWNrZXQpXCIsXCJuYW1lXCI6XCIkKHg6bmFtZSlcIn0iLCJkZWFkbGluZSI6MTc4MjczNTczMn0=",
                "expireTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "static_visit_host": "http://cdn.imgresource.com.cn"
            },
            "msg": "ok"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })




