import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException,Request

from app.db.models import AdminRole
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
from app.models.admin import AdminLoginParams, AddAdmin, EditAdmin, DelAdmin, GetAdminList

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

# @router.get("/getCaptcha",description="获取验证码返回图片",summary="获取验证码")
# def getCaptcha():
#     # 随机4位验证码
#     code = ''.join(
#         random.choices(string.ascii_uppercase + string.digits, k=4)
#     )
#
#     image = ImageCaptcha()
#
#     data = image.generate(code)
#
#     # 这里应该把 code 存 Redis（后面讲）
#     print("验证码答案:", code)
#
#     return StreamingResponse(
#         data,
#         media_type="image/png"
#     )

@router.get("/getCaptcha",description="获取验证码返回图片",summary="获取验证码", response_model = ResStructure)
async def get_captcha():

    """
    返回 base64 验证码
    """

    # 1. 随机生成4位验证码
    code = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=4
        )
    )

    # 2. 创建验证码图片对象
    image = ImageCaptcha()

    # 3. 写入内存
    buffer = BytesIO()
    image.write(code, buffer)

    # 4. 转 base64
    img_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    # 5. 生成唯一ID（给前端回传）
    captchaKey = str(uuid.uuid4())
    await redis_manager.db0.setex(captchaKey, 60, code) # 60秒后过期
    # await redis_manager.db0.set(captchaKey, code, ex=60) # 60秒后过期
    # await redis_manager.db0.set(captchaKey, code, px=60000)  # 60秒后过期,毫秒为单位

    return success({
        "data": {
            "captchaKey": captchaKey,
            # "captchaBase64": "data:image/svg+xml;base64," + img_base64,
            "captchaBase64": "data:image/png;base64," + img_base64,
        },
        "msg": "ok"
    })



@router.post("/login", description="登录",summary="登录", response_model=ResStructure, response_model_exclude_none=True)
async def login(
        body:AdminLoginParams,
        db: Session = Depends(get_db),
        request: Request = None
):
    client_info = get_client_info(request)
    code = await redis_manager.db0.get(body.captchaKey)
    if code != body.captchaCode:
        raise HTTPException(400, '验证码错误')
    try:
        result: Any | None = db.query(
            Admin.id,
            Admin.name,
            Admin.phone,
            Admin.password,
            Admin.last_login_time,
            Admin.status,
            Admin.role_id,
            Admin.avatar,
        ).filter(
            Admin.phone == body.phone,
            Admin.delete_time.is_(None),
        ).first()

        if not result:
            raise HTTPException(400, '账户或密码错误')

        if not verify_password(body.password, result.password):
            raise HTTPException(400,'账户或密码错误')

        if result.status in [0]:
            raise HTTPException(400,'该账号无权限登录！！！')

        token = create_access_token({"id": result.id})


        r_d = dict(result._mapping)
        last_login_time = datetime.datetime.now()
        r_d["last_login_time"] = str(last_login_time.strftime("%Y-%m-%d %H:%M:%S"))
        del r_d['password']

        db.query(Admin).filter(Admin.id == result.id).update({
            Admin.last_login_time: last_login_time,
        })
        admin_login_log = AdminLoginLog(
            admin_id = result.id,
            ip = client_info['ip'],
            login_time = datetime.datetime.now(),
            user_agent = client_info['user_agent'],
        )
        db.add(admin_login_log)
        db.commit()
        return success({
            "code": 200,
            "data": {
                "admin":{
                    **r_d
                },
                "accessToken": token,
            },
            "msg": "登录成功"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })



# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/getList",description="获取管理员列表",summary="获取管理员列表", response_model = ResStructure)
async def get_list(
    body: GetAdminList,
    db: Session = Depends(get_db),
    admin=Depends(login_auth_guard),
):
    print("body=======",body)
    page = body.page or 1
    limit = body.limit or 10
    offset = (page - 1) * limit


    query = db.query(Admin,AdminRole.role_name).outerjoin(AdminRole, Admin.role_id==AdminRole.id)
    print("进来了吗===》〉body111", body.status, body,page,limit)

    query = query.filter(Admin.delete_time.is_(None))
    if body.keywords:
        query = query.filter(func.concat(Admin.name, Admin.phone).like(
            func.concat("%", body.keywords, "%")
        ))
    if body.status in [0,1]:
        query = query.filter(Admin.status == body.status)

    count = query.count()

    query = query.order_by(Admin.id.desc())
    query = query.offset(offset).limit(limit)
    data = query.all()

    obj = {
        0: "禁用",
        1: "启用"
    }

    result = [
        {
            "id": admin.id,
            "avatar": admin.avatar,
            "phone": admin.phone,
            "name": admin.name,
            "status": admin.status,
            "status_name": obj.get(admin.status),
            "role_id": admin.role_id,
            "role_name": role_name,
            "delete_time": admin.delete_time.strftime("%Y-%m-%d %H:%M:%S") if admin.delete_time else None,
            "created_at": admin.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": admin.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login_time": admin.last_login_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for admin, role_name in data
    ]
    return success({
        "data": {
            "rows": result,
            "count": count,
        },
        "msg": "ok"
    })

# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/add", description="添加管理员",summary="添加管理员", response_model=ResStructure, response_model_exclude_none=True)
async def add(
        body: AddAdmin,
        db: Session = Depends(get_db),
        # admin=Depends(login_auth_guard)
):
    try:
        exist = db.query(Admin).filter(
            Admin.phone == body.phone,
            Admin.delete_time.is_(None),
        ).first()
        if exist:
            raise HTTPException(400, '账号已经存在')

        if body.role_id:
            role = db.query(AdminRole).filter(
                AdminRole.id == body.role_id,
                AdminRole.delete_time.is_(None),
            ).first()
            if not role:
                raise HTTPException(400, '角色不存在！！！')

        admin = Admin(
            phone=body.phone,
            password=hash_password(body.password),
            name=body.name,
            status=body.status if body.status else 1,
            role_id=body.role_id if body.role_id else None,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            avatar=body.avatar if body.avatar else None,
        )
        db.add(admin)
        """
            db.flush()  #获取ID
            admin_id = admin.id  # 可以通过 执行 db.flush() 后提前获取 admin.id 无需  db.commit() 后 再执行db.refresh(admin)刷新才能获取admin.id
        """
        db.commit()
        db.refresh(admin)  # 刷新 SQLAlchemy 对象才能获取 到admin.id
        return success({
            "data": {
                "id": admin.id
            },
            "msg": "ok"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })


# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/edit", description="编辑管理员",summary="编辑管理员", response_model=ResStructure, response_model_exclude_none=True)
async def edit(
        body: EditAdmin,
        db: Session = Depends(get_db),
        admin = Depends(login_auth_guard)
):
    try:
        exist = db.query(Admin).filter(
            Admin.id == body.id,
            Admin.delete_time.is_(None),
        ).first()
        if not exist:
            raise HTTPException(400, '数据不存在')

        if body.role_id:
            role = db.query(AdminRole).filter(
                AdminRole.id == body.role_id,
                AdminRole.delete_time.is_(None),
            ).first()
            if not role:
                raise HTTPException(400, '角色不存在！！！')

        db.query(Admin).filter(Admin.id == body.id).update({
            Admin.phone: body.phone,
            Admin.name: body.name,
            Admin.status: body.status,
            Admin.role_id: body.role_id,
            Admin.updated_at: datetime.datetime.now(),
            Admin.avatar: body.avatar,
        })
        db.commit()
        return success({
            "msg": "编辑成功"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })


# response_model 设定响应结构，response_model_exclude_none 为true 有传某个属性时才返回
@router.post("/del", description="删除管理员",summary="删除管理员", response_model=ResStructure, response_model_exclude_none=True)
async def deleted(
        body: DelAdmin,
        db: Session = Depends(get_db),
        admin = Depends(login_auth_guard)
):
    try:
        exist = db.query(Admin).filter(
            Admin.id == body.id,
            Admin.delete_time.is_(None),
        ).first()
        if not exist:
            raise HTTPException(400, '数据不存在')

        db.query(Admin).filter(Admin.id == body.id).update({
            Admin.updated_at: datetime.datetime.now(),
            Admin.delete_time: datetime.datetime.now(),
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
@router.post("/getInfo", description="获取登录信息",summary="获取登录信息", response_model=ResStructure, response_model_exclude_none=True)
async def getInfo(
        db: Session = Depends(get_db),
        admin = Depends(login_auth_guard)
):
    try:
        exist = db.query(
            Admin.name,
            Admin.id,
            Admin.phone,
            Admin.status,
            Admin.updated_at,
            Admin.delete_time,
            Admin.created_at,
            Admin.role_id,
            Admin.avatar,
        ).filter(
            Admin.id == admin.id,
            Admin.delete_time.is_(None),
        ).first()
        if not exist:
            raise HTTPException(400, '数据不存在')

        data = dict(exist._mapping)

        return success({
            "data": data,
            "msg": "ok"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": getattr(e, "detail", str(e)),
        })