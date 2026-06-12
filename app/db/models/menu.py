from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base
from sqlalchemy.dialects.mysql import TINYINT,DOUBLE,TEXT,JSON,INTEGER

class Menu(Base):
    __tablename__ = "menu"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)

    path = Column(String(50), nullable=True,comment="访问路径")

    name = Column(String(50), nullable=True, comment="菜单名称")

    component = Column(String(50), nullable=True, comment="组件目录")

    redirect = Column(String(50), nullable=True, comment="路由重定向")

    meta = Column(JSON, nullable=True)

    pid = Column(Integer, nullable=True, comment="父id")

    updated_at = Column(DATETIME(), nullable=True)

    created_at = Column(DATETIME(), nullable=True)

    delete_time = Column(DATETIME(), nullable=True)


    status = Column(TINYINT(1),
                    default=1,
                    nullable=False,
                    comment="状态 0: 禁用 1:启用")

    role_ids = Column(String(255), nullable=False, comment="角色权限")

    admin_ids = Column(String(255), nullable=False, comment="单个管理员权限")


    sort = Column(Integer, nullable=False)




