from fastapi import APIRouter,Query,HTTPException,Depends,Header
from fastapi.exceptions import RequestValidationError
from fastapi.security import oauth2

from app.models.item import CreateItemParams,CreateItemResponse

from app.utils.httpRes import success,fail,ResStructure
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()

security = HTTPBearer()

# 模拟数据库
fake_items_db = []


'''
    ... 表示必填
    min_length / max_length → 字符串长度限制
    ge（greater or equal）/ le（less or equal） → 数字范围
    
    只要给参数一个默认值（比如 None 或其他值），FastAPI 就会把它当作可选参数
'''
@router.get("/items")
def get_items(
        name: str = Query(..., min_length=2, max_length=3, description="商品名称"),
        price: float = Query(0, ge=0, le=1000, description="商品价格")
    ):
    fake_items_db.append({"name": name, "price": price})
    return {"items": fake_items_db}


# def auth_guard(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(401, "未登录")
#     return {"user_id": 1}

def auth_guard(
    aaa: HTTPAuthorizationCredentials = Depends(security)
):
    print('----',aaa)
    token = aaa.credentials  # 自动去掉 Bearer
    if token != "123456":
        raise HTTPException(401, "token 无效")
    return {"user_id": 1}

@router.post("/items",response_model=ResStructure)
def create_item(user=Depends(auth_guard)):
    print('accessionToken==>>', user)
    return success({
        "code": 200,
        "data": '12345',
        "message": "操作成功"
    })

    # try:
    #     if len(item.name) <= 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="名字长度不能小于两个字符",
    #         )
    #         # raise Exception("名字长度不能小于两个字符")
    #     fake_items_db.append(item.model_dump())
    #     return success({
    #         "code": 200,
    #         "data": fake_items_db,
    #         "message": "操作成功"
    #     })
    # except Exception as e:
    #     raise

