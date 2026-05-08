
from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,Any, List
from fastapi import Request
from datetime import datetime

class ResStructure(BaseModel):
    code: int
    data: Any | None = None
    msg: str | None = None




def fail(data: dict):
    res = {
        "code": data.get("code", 400)
    }
    if data.get("data"):
        res['data'] = data.get("data")
    if data.get("msg"):
        res.update({"msg": data.get("msg")})
    if data.get("path"):
        res.update({"path": data.get("path")})

    res.update({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return res
def success(data: dict):
    res = {
        "code": data.get("code", 200)
    }
    if data.get("data"):
        res['data'] = data.get("data")
    if data.get("msg"):
        res.update({"msg": data.get("msg")})
    if data.get("path"):
        res.update({"path": data.get("path")})
    res.update({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return res