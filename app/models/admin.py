from pydantic import BaseModel,Field,ConfigDict, field_validator
from typing import Optional,List

'''
    必传字段
        Field(..., ...) 里的 ... 表示必填。
        如果给了默认值（包括 None），则变成可选字段。
    字符串限制
        min_length=1：最少 1 个字符
        max_length=50：最多 50 个字符
    数字限制
        ge=0：greater or equal，大于等于 0
        le=1000：less or equal，小于等于 1000
    文档描述
        description="xxx" 会显示在 Swagger UI 中
'''


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
    password: str = Field(..., min_length=6, max_length=32, description="密码长度6-32位")
    name: str  = Field(..., min_length=2, max_length=32, description="姓名密码长度2-32位")
    status: int = Field(..., ge=0,le=1, description="status状态必须是0，1")
    avatar: str  = Field(..., description="头像")
    role_id: str  = Field('', description="所属角色")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        v= v.replace(" ", "")
        if len(v) != 11:
            raise ValueError("手机号必须11位")

        return v
