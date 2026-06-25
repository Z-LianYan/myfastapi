import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException,Request

from app.db.models import AdminRole
from app.db.models.admin_role import AdminRoleVO
from app.utils.httpRes import ResStructure
from jose import jwt
from app.core.config import settings
from captcha.image import ImageCaptcha
import random
import string
import uuid
from io import BytesIO
import base64
from app.utils.httpRes import success,fail
from app.redis.redis import redis_manager
from app.models.adminRole import GetAdminRoleList, AddAdminRole, EditAdminRole, DelAdminRole


from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models.admin import Admin
from app.db.models.admin_login_log import AdminLoginLog
from app.core.guards.authLogin import login_auth_guard
router = APIRouter()
from app.utils.password import hash_password,verify_password
from app.utils.joseJwt import create_access_token,verify_access_token
from app.utils import get_client_info


# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/getList",description="获取管理员角色",summary="角色列表", response_model = ResStructure)
async def get_list(
    body: GetAdminRoleList,
    db: Session = Depends(get_db),
    admin=Depends(login_auth_guard),
):
    print("body=======",body)
    page = body.page or 1
    limit = body.limit or 10
    offset = (page - 1) * limit


    query = db.query(AdminRole)
    print("进来了吗===》〉body111", body.status, body,page,limit)


    if body.keywords:
        query = query.filter(AdminRole.role_name.like(f"%{body.keywords}%"))
    if body.status:
        query = query.filter(AdminRole.status == body.status)

    count = query.count()

    query = query.order_by(AdminRole.id.desc())
    query = query.offset(offset).limit(limit)
    data = query.all()

    obj = {
        0: "禁用",
        1: "启用"
    }


    result = [
        {
            "id": item.id,
            "role_name": item.role_name,
            "status": item.status,
            "status_name": obj.get(item.status),
            "remark": item.remark,
            "delete_time": item.delete_time.strftime("%Y-%m-%d %H:%M:%S") if item.delete_time else None,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for item in data
    ]
    return success({
        "data": {
            "rows": result,
            "count": count,
        },
        "msg": "ok"
    })


 # response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/add", description="添加管理员角色",summary="添加管理员角色", response_model=ResStructure, response_model_exclude_none=False)
async def add(
    body: AddAdminRole,
    db: Session = Depends(get_db),
    admin = Depends(login_auth_guard),
    request: Request = None
):
    try:
        row = db.query(AdminRole).filter(
            AdminRole.role_name == body.role_name,
            AdminRole.delete_time.is_(None)
        ).first()
        if row is not None:
            raise HTTPException(status_code=400, detail="角色已经存在")

        admin_role = AdminRole(
            role_name=body.role_name,
            status=body.status,
            remark=body.remark,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        db.add(admin_role)
        db.commit()
        return success({
            "code": 200,
            "data": {
                "row": {
                    c.name: getattr(admin_role, c.name)
                    for c in admin_role.__table__.columns
                },
                "data": AdminRoleVO.model_validate(admin_role)
            }
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })


 # response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/edit", response_model=ResStructure, response_model_exclude_none=False)
async def edit(
        body: EditAdminRole,
        db: Session = Depends(get_db),
        admin=Depends(login_auth_guard)
):
    try:
        exist = db.query(AdminRole).filter(
            AdminRole.id == body.id,
            AdminRole.delete_time.is_(None),
        ).first()
        if not exist:
            raise HTTPException(400, '数据不存在')

        db.query(AdminRole).filter(AdminRole.id == body.id).update({
            AdminRole.role_name: body.role_name,
            AdminRole.remark: body.remark,
            AdminRole.status: body.status,
            AdminRole.updated_at: datetime.datetime.now(),
        })
        db.commit()
        return success({
            "msg": "修改成功"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })

 # response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/del", response_model=ResStructure, response_model_exclude_none=False)
async def deleted(
        body: DelAdminRole,
        db: Session = Depends(get_db),
        admin_login=Depends(login_auth_guard)
):
    try:
        exist = db.query(AdminRole).filter(
            AdminRole.id == body.id,
            AdminRole.delete_time.is_(None),
        ).first()
        if not exist:
            raise HTTPException(400, '数据不存在')

        db.query(AdminRole).filter(AdminRole.id == body.id).delete()
        db.commit()
        return success({
            "msg": "删除成功"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })

