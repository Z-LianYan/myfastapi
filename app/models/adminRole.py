from pydantic import BaseModel,Field,ConfigDict, field_validator
from typing import Optional,List,Literal

from enum import IntEnum

class StatusEnum(IntEnum):
    DISABLED = 0
    ENABLED = 1

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


class GetAdminRoleList(BaseModel):
    page: str = Field(..., description="分页页数")
    limit: str = Field(..., description="每页获取数据条数")
    keywords: str  = Field(..., description="关键字搜索: 角色名称")
    status: str = Field(None, description="状态")



class AddAdminRole(BaseModel):
    role_name: str = Field(..., description="角色名称")
    # status: int = Field(..., ge=0, le=1, description="状态")
    remark: str  = Field(None, min_length=0, max_length=150, description="备注")
    status: Literal[0, 1] = Field(
        ...,
        description="状态：0禁用，1启用"
    )

    @field_validator("role_name")
    @classmethod
    def validate_role_name(cls, v):
        if not v.strip():
            raise ValueError("角色名称不能为空")
        return v


class EditAdminRole(BaseModel):
    id: int = Field(..., description="角色id")
    role_name: str = Field(..., description="角色名称")
    status: Literal[0, 1] = Field(
        ...,
        description="状态：0禁用，1启用"
    )
    remark: str | None  = Field(None, min_length=0, max_length=150, description="备注")

    @field_validator("id")
    @classmethod
    def validate_role_name(cls, v):
        if not v:
            raise ValueError("id不能为空")
        return v

    @field_validator("role_name")
    @classmethod
    def validate_role_name(cls, v):
        if not v.strip():
            raise ValueError("角色名称不能为空")
        return v

class DelAdminRole(BaseModel):
    id: int = Field(..., description="角色id")