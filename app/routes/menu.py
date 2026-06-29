import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException,Request

from app.db.models import AdminRole,Menu
from app.utils.httpRes import ResStructure
from app.utils.httpRes import success,fail
from app.models.menu import GetMeneList, AddMenu, EditMenu, DelMenu


from sqlalchemy import func, or_, and_, text, select
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.guards.authLogin import login_auth_guard
router = APIRouter()
import json


def handle_menu(rows):
    lists = []
    for item in rows:
        if not item.get("children"):
            item["children"] = []
        for it in rows:
            if item.get("id") == it.get("pid"):
                item["children"].append(it)

    for item in rows:
        if item.get("pid")==0:
            lists.append(item)
    return lists

def filter_menu(rows, keywords=None):
    menus = []
    for item in rows:
        if keywords:
            if item.get("meta").get("title") .find(keywords) != -1:
                menus.append(item)
            elif  item.get("children") and len(item.get("children")):
                item['children'] = filter_menu(item['children'], keywords)
                if item.get("children") and len(item.get("children")):
                    menus.append(item)
        else:
            menus.append(item)
            item['children'] = filter_menu(item.get("children") or [], keywords)

    # sorted()：返回一个新的排序结果，不修改原数据。
    # list.sort()：原地排序，会修改原列表。=
    menus.sort(key=lambda x: x.get("sort") or 0)
    return menus


# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/getList",description="获取菜单列表",summary="获取菜单列表", response_model = ResStructure)
async def get_list(
    body: GetMeneList,
    db: Session = Depends(get_db),
    admin=Depends(login_auth_guard),
):
    try:
        page = body.page or 1
        limit = body.limit or 10
        offset = (page - 1) * limit

        query = db.query(Menu)
        query = query.filter(Menu.delete_time.is_(None))

        if body.status in [0, 1]:
            query = query.filter(Menu.status == body.status)

        query = query.order_by(Menu.id.desc())
        data = query.all()

        obj = {
            0: "禁用",
            1: "启用"
        }
        # data 是  <class 'list'> 才能使用这个方式处理放回前端
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

        menus = handle_menu(result)
        # if body.keywords:
        menus = filter_menu(menus, body.keywords)

        menus = menus[offset : offset + limit]
        count = len(menus)

        return success({
            "data": {
                "rows": menus,
                "count": count
            },
            "msg": "ok"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
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



# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/routes", description="获取管理员授权菜单",summary="获取管理员授权菜单", response_model=ResStructure, response_model_exclude_none=False)
async def routes(
        db: Session = Depends(get_db),
        admin=Depends(login_auth_guard)
):
    try:
        conditions = [
            and_(
                Menu.admin_ids.is_(None),
                Menu.role_ids.is_(None),
            )
        ]

        if admin.role_id is not None:
            conditions.append(
                func.find_in_set(admin.role_id, Menu.role_ids) > 0
            )

        conditions.append(
            func.find_in_set(admin.id, Menu.admin_ids) > 0
        )
        stmt = select(Menu).where(or_(*conditions),Menu.delete_time.is_(None))

        # data = db.query(Menu).filter(
        #     or_(*conditions),
        #     Menu.delete_time.is_(None),
        # ).all()

        # data = db.execute(stmt).mappings().all()
        data = db.execute(stmt).scalars().all()
        # sql = text("""
        #     SELECT *
        #     FROM menu
        #     WHERE (
        #         FIND_IN_SET(:role_id, role_ids)
        #         OR FIND_IN_SET(:admin_id, admin_ids)
        #         OR (role_ids IS NULL AND admin_ids IS NULL)
        #     )
        #     AND delete_time IS NULL
        # """)
        #
        # data = db.execute(
        #     sql,
        #     {
        #         "role_id": admin.role_id,
        #         "admin_id": admin.id,
        #     }
        # ).mappings().all()
        #
        # print("data====>>111",type(data))
        obj = {
            0: "禁用",
            1: "启用"
        }

        """
            json.loads(item.meta)
            json.dumps({"a": 1})
        """
        result = [
            {
                "id": item.id,
                "path": item.path,
                "name": item.name,
                "component": item.component,
                "redirect": item.redirect,
                "meta":  item.meta,
                # "meta":  json.loads(item.meta) if item.meta else {},
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

        result = handle_menu(result)

        menus = filter_menu(result)

        return success({
            "data": menus,
            "msg": "ok"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })



