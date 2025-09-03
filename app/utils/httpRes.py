
from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,Any, List

class ResStructure(BaseModel):
    code: int
    data: Any
    message: str | None = None




def fail(data: dict):
    res = {
        "code": data.get("code", 400)
    }
    if data.get("data"):
        res['data'] = data.get("data")
    if data.get("message"):
        res.update({"message": data.get("message")})
    if data.get("path"):
        res.update({"path": data.get("path")})
    return res
def success(data: dict):
    res = {
        "code": data.get("code", 200)
    }
    if data.get("data"):
        res['data'] = data.get("data")
    if data.get("message"):
        res.update({"message": data.get("message")})
    if data.get("path"):
        res.update({"path": data.get("path")})
    return res