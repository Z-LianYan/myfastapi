from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,List

class AdminLoginParams(BaseModel):
    phone: str = Field(..., min_length=1, max_length=50, description="商品名称，1-50个字符")
    password: float = Field(..., ge=0, le=1000, description="商品价格，0-1000之间")
    captchaCode: str  = Field(None, min_length=4, max_length=4, description="验证码，长度4位")
    captchaKey: str | None = Field(None, max_length=200, description="商品描述，最多200个字符")