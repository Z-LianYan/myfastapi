from pydantic import BaseModel,Field,ConfigDict, field_validator
from typing import Optional,List
class AdminLoginParams(BaseModel):
    phone: str = Field(..., description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    captchaCode: str  = Field(..., min_length=4, max_length=4, description="验证码")
    captchaKey: str = Field(..., max_length=200, description="验证码key")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        v= v.replace(" ", "")
        if len(v) != 11:
            raise ValueError("手机号必须11位")

        return v

class AdminAddParams(BaseModel):
    phone: str = Field(..., description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    name: str  = Field(..., min_length=2, max_length=32, description="姓名")
    status: int = Field(..., max_digits=1, description="status状态必须是0，1")
    avatar: str  = Field(..., description="头像")


    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        v= v.replace(" ", "")
        if len(v) != 11:
            raise ValueError("手机号必须11位")

        return v
