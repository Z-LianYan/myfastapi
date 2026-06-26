import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException,Request

from app.db.models import AdminRole,Menu
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
from app.models.menu import GetMeneList, AddMenu, EditMenu, DelMenu


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


def handle_menu(rows):
    lists = []
    for item in rows:
        if item.get("children"):
            item["children"] = []
        for it in rows:
            if item.get("id") == it.get("pid"):
                item["children"].append(it)

    for item in rows:
        if item.pid==0:
            lists.append(item)
    return lists

# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/getList",description="获取菜单列表",summary="获取菜单列表", response_model = ResStructure)
async def get_list(
    body: GetMeneList,
    db: Session = Depends(get_db),
    # admin=Depends(login_auth_guard),
):
    print("body=======",body)
    page = body.page or 1
    limit = body.limit or 10
    offset = (page - 1) * limit


    query = db.query(Menu)
    print("进来了吗===》〉body111", body.status, body,page,limit)


    # if body.keywords:
    #     query = query.filter(Menu.role_name.like(f"%{body.keywords}%"))
    if body.status:
        query = query.filter(Menu.status == body.status)

    query = query.order_by(Menu.id.desc())
    data = query.all()

    obj = {
        0: "禁用",
        1: "启用"
    }

    result = [
        {
            "id": item.id,
            "path": item.path,
            "name": item.name,
            "component": item.component,
            "redirect": item.redirect,
            "meta": item.meta,
            "pid": item.pid,
            "role_ids": item.role_ids.split(",") if item.role_ids else [],
            "admin_ids": item.admin_ids.split(",") if item.admin_ids else [],
            "sort": item.sort,
            "status": item.status,
            "status_name": obj.get(item.status),
            "delete_time": item.delete_time.strftime("%Y-%m-%d %H:%M:%S") if item.delete_time else None,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for item in data
    ]




    # result = handle_menu(result)


    # print("data=======",data)
    # ls = []
    # for item in result:
    #     print(type(item),item['path'])
    #
    # s = "2,3,4"
    # print('s--------->',s,s.split(","))


    return success({
        "data": {
            "rows": result,
            # "count": count,
            # "ls": ls
        },
        "msg": "ok"
    })


 # response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/add", description="添加菜单",summary="添加菜单", response_model=ResStructure, response_model_exclude_none=False)
async def add(
    body: AddMenu,
    db: Session = Depends(get_db),
    admin = Depends(login_auth_guard),
    request: Request = None
):
    try:
        if body.pid:
            exist = db.query(Menu).filter(
                Menu.id == body.pid,
                Menu.delete_time.is_(None),
            ).first()
            if not exist:
                raise HTTPException(400, detail="pid 不存在")


        menu = Menu(
            path=body.path,
            name=body.name,
            component=body.component,
            redirect=body.redirect or None,
            meta=body.meta,
            pid=body.pid,
            status=body.status,
            role_ids=body.role_ids,
            admin_ids=body.admin_ids,
            sort=body.sort,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

        db.add(menu)
        db.commit()
        return success({
            "code": 200,
            "data": {
                "row": {
                    c.name: getattr(menu, c.name)
                    for c in menu.__table__.columns
                }
            }
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })


 # response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/edit", description="编辑菜单",summary="编辑菜单", response_model=ResStructure, response_model_exclude_none=True)
async def edit(
        body: EditMenu,
        db: Session = Depends(get_db),
        admin=Depends(login_auth_guard)
):
    try:
        exist = db.query(Menu).filter(
            Menu.id == body.id,
            Menu.delete_time.is_(None),
        ).first()
        if not exist:
            raise HTTPException(400, '数据不存在')

        db.query(Menu).filter(Menu.id == body.id).update({
            Menu.path: body.path,
            Menu.name: body.name,
            Menu.component: body.component,
            Menu.redirect: body.redirect or None,
            Menu.meta: body.meta,
            Menu.pid: body.pid,
            Menu.status: body.status,
            Menu.role_ids: body.role_ids,
            Menu.admin_ids: body.admin_ids,
            Menu.sort: body.sort,
            Menu.updated_at: datetime.datetime.now(),
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
@router.post("/del", description="删除菜单",summary="删除菜单", response_model=ResStructure, response_model_exclude_none=False)
async def deleted(
        body: DelMenu,
        db: Session = Depends(get_db),
        admin_login=Depends(login_auth_guard)
):
    try:
        exist = db.query(Menu).filter(
            Menu.id == body.id,
            Menu.delete_time.is_(None),
        ).first()

        if not exist:
            raise HTTPException(400, '数据不存在')

        db.query(Menu).filter(Menu.id == body.id).update({
            Menu.delete_time: datetime.datetime.now(),
            Menu.updated_at: datetime.datetime.now(),
        })
        db.commit()
        return success({
            "msg": "删除成功"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })

