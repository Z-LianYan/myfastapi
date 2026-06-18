import datetime

from fastapi import APIRouter, Depends, HTTPException

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
from app.models.admin import AdminLoginParams, AdminAddParams

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models.admin import Admin
from app.core.guards.authLogin import login_auth_guard
router = APIRouter()
from app.utils.password import hash_password,verify_password
from app.utils.joseJwt import create_access_token,verify_access_token


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


# def create_item(user=Depends(login_auth_guard)):
@router.post("/login", response_model=ResStructure, response_model_exclude_none=True)
async def login(
        body:AdminLoginParams,
        db: Session = Depends(get_db)
):
    code = await redis_manager.db0.get(body.captchaKey)
    print('accessionToken==>>', "user", code,body.captchaCode)
    # if(code != body.captchaCode):
    #     raise HTTPException(400, '验证码错误')





    try:


        result = db.query(Admin).filter(
                    Admin.phone == body.phone,
                ).offset(0).limit(10).one()

        token = create_access_token({"id": result.id})
        v_res = verify_password(body.password, result.password)
        if not v_res:
            raise HTTPException(400,'账户或密码错误')


        return success({
            "code": 200,
            "data": {
                "data": "11",
                "token": token,
            },
            "msg": "操作成功"
        })
    except Exception as e:
        return fail({
            "code": 400,
            "msg": e.detail
        })




@router.post("/add", response_model=ResStructure, response_model_exclude_none=True)
async def add(
        body:AdminAddParams,
        db: Session = Depends(get_db)
):
    print("======>>11",body.__dict__,body.password,hash_password(body.password))
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
    db.refresh(admin) # 刷新 SQLAlchemy 对象才能获取 到admin.id

    print("======>>222",verify_password(body.password, admin.password), admin.__dict__)

    # raise HTTPException(400,'1111')

    return success({
        "data": {
            "id": admin.id
        },
        "msg": "ok"
    })
