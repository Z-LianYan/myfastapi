import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException,Request

from app.utils.httpRes import ResStructure
from app.utils.httpRes import success,fail

from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.guards.authLogin import login_auth_guard
router = APIRouter()
import json
from app.core.config import settings
from datetime import datetime, timedelta
import math
from qiniu import Auth

# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/getQiNiuToken",description="获取上传七牛云token",summary="获取上传七牛云token", response_model = ResStructure)
async def get_list(
    db: Session = Depends(get_db),
    admin=Depends(login_auth_guard),
):
    try:
        # -*- coding: utf-8 -*-
        # flake8: noqa

        # 需要填写你的 Access Key 和 Secret Key
        access_key = ''
        secret_key = ''
        # 构建鉴权对象
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
        # 要上传的空间
        bucket_name = settings.QINIU_BUCKET
        # 上传后保存的文件名
        # key = math.floor(datetime.now().timestamp())
        key = None
        # 生成上传 Token，可以指定过期时间等
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        policy = {
            # 'callbackUrl':'https://requestb.in/1c7q2d31',
            # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
            # 'persistentOps':'imageView2/1/w/200/h/200'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        expires = 3600
        token = q.upload_token(bucket_name, key, expires, policy)
        print("settings===>>QINIU_BUCKET",bucket_name, token)


        return success({
            "data": {
                "upload_token": token,
                "expireTime": (datetime.now() + timedelta(seconds=expires)).strftime("%Y-%m-%d %H:%M:%S"),
                "static_visit_host": settings.QINIU_STATIC_HOST
            },
            "msg": "ok"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })




