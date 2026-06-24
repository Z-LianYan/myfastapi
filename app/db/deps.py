from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception: # 这个异常处理可以忽略，因为db.close 回去处理，写出是为了更好的理解
        db.rollback()
        raise
    finally:
        db.close()
        # 释放 Session 持有的连接
        # 清空 Session 缓存
        # 未提交事务会回滚