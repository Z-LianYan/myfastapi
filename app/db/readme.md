 # 集成 sqlalchemy 


## ========== main.py 文件内容 ==========
```bash
# 导入所有模型
from app.db.models.init import *
from app.db.base import Base
# print(Base.metadata.tables)
from app.db.session import engine
# 自动创建表
Base.metadata.create_all(bind=engine)
```


## ============ 使用例子 ===========
```bash
    from fastapi import Depends
    from app.db.deps import get_db
    from sqlalchemy.orm import Session
    
    @router.post("/login", response_model=ResStructure)
    def create_item(
            db: Session = Depends(get_db)
    ):
        try:
            result = db.query(User).all()
            print("sql===>>",result)
        except Exception as e:
            print("exception===>", e)
```
            
