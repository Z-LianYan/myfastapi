from pydantic import BaseModel,Field,ConfigDict, field_validator
from typing import Optional,List
from typing import Optional,List,Literal,Any

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

class GetMeneList(BaseModel):
    page: int | None = Field(None, description="分页页数")
    limit: int | None = Field(None, description="每页获取数据条数")
    keywords: str | None  = Field('', description="关键字搜索: 菜单名称")
    status: str | None = Field(None, description="状态 0禁用 1启用")


class Meta(BaseModel):
    icon: str = Field(..., description="图标")
    affix: int = Field(..., description="是否一直显示在历史菜单不可关闭（TagsView中显示）")
    title: str = Field(..., description="菜单名称")
    hidden: int = Field(..., description="路由标题")
    keepAlive: int = Field(..., description="是否缓存")
    alwaysShow: int = Field(..., description="当只有一个子路由时是否始终显示父级菜单")


class AddMenu(BaseModel):
    path: str = Field(..., description="访问路径")
    name: str = Field(..., min_length=1, max_length=32, description="路由名称")
    component: str = Field(..., min_length=1, max_length=4, description="组件目录")
    redirect: str | None = Field("", max_length=200, description="路由重定向")
    # meta: Meta = Field(..., description="元数据")
    meta: dict[str, Any] = Field(
        default_factory=dict,
        description="元数据"
    )
    pid: int = Field(..., ge=0, description="父id")
    status: Literal[0, 1] = Field(
        ...,
        description="状态：0禁用，1启用"
    )
    role_ids: str = Field(..., min_length=1, max_length=9999, description="角色权限")
    admin_ids: str = Field(..., min_length=1, max_length=9999, description="管理员权限")
    sort: int = Field(..., ge=1, description="排序")

class EditMenu(BaseModel):
    id: int = Field(..., description="菜单id")
    path: str = Field(..., description="访问路径")
    name: str = Field(..., min_length=1, max_length=32, description="菜单名称")
    component: str = Field(..., min_length=1, max_length=4, description="组件目录")
    redirect: str | None = Field("", max_length=200, description="路由重定向")
    # meta: Meta = Field(..., description="元数据")
    meta: dict[str, Any] = Field(
        default_factory=dict,
        description="元数据"
    )
    pid: int = Field(..., ge=1, description="父id")
    status: Literal[0, 1] = Field(
        ...,
        description="状态：0禁用，1启用"
    )
    role_ids: str = Field(..., min_length=1, max_length=9999, description="角色权限")
    admin_ids: str = Field(..., min_length=1, max_length=9999, description="管理员权限")
    sort: int = Field(..., ge=1, description="排序")

class DelMenu(BaseModel):
    id: int = Field(...,description="菜单id")

    @field_validator("id")
    @classmethod
    def validate_admin_id(cls, v):
        if not v:
            raise ValueError("缺少菜单id")

        return v
