from pydantic import BaseModel,Field,ConfigDict
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
# 定义数据模型
class CreateItemParams(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="商品名称，1-50个字符")
    price: float = Field(..., ge=0, le=1000, description="商品价格，0-1000之间")
    description: str | None = Field(None, max_length=200, description="商品描述，最多200个字符")



class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    # 忽略未定义字段
    # model_config: ConfigDict = ConfigDict(extra="ignore")

class CreateItemResponse(BaseModel):
    msg: str
    item: List[Item]