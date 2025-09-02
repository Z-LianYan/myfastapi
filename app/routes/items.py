from fastapi import APIRouter,Query,HTTPException
from app.models.item import CreateItemParams,CreateItemResponse





router = APIRouter()

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


@router.post("/items", response_model=CreateItemResponse)
def create_item(item: CreateItemParams):
    fake_items_db.append(item.model_dump())
    # print("<UNK>",item.name)
    if item.name: raise HTTPException(status_code=401, detail="Missing age")
    return {"message": "Item created successfully", "item": fake_items_db}
