from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,List

class AdminLoginParams(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11,title="手机号", description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    captchaCode: str  = Field(..., min_length=4, max_length=4, description="验证码")
    captchaKey: str = Field(..., max_length=200, description="captchaKey")