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
