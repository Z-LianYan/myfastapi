from fastapi import APIRouter, Query, HTTPException, Depends, Header, Request, Response

from app.utils.httpRes import success, fail, ResStructure
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.guards.authLogin import login_auth_guard
from jose import jwt
from app.core.config import settings
from fastapi.responses import StreamingResponse
from captcha.image import ImageCaptcha
import random
import string
import uuid
from io import BytesIO
import base64
from app.utils.httpRes import success,fail
from fastapi import Request

router = APIRouter()

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

@router.get("/getCaptcha",description="获取验证码返回图片",summary="获取验证码")
def get_captcha():
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

    # 这里应该存 Redis（后面讲）
    print("captchaKey =", captchaKey)
    print("答案 =", code)

    return success({
        "data": {
            "captchaKey": captchaKey,
            "captchaBase64": img_base64,
        },
        "message": "ok"
    })


# def create_item(user=Depends(login_auth_guard)):
@router.post("/login", response_model=ResStructure)
def create_item():
    print('accessionToken==>>', "user")
    token = jwt.encode(
        {"a":"to_encode"},
        settings.JWT_SECRET, # 密钥
        algorithm="HS256" # 加密算法
    )
    return success({
        "code": 200,
        "data": token,
        "message": "操作成功"
    })

