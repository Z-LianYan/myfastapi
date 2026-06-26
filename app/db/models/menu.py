from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base
from sqlalchemy.dialects.mysql import TINYINT,DOUBLE,TEXT,JSON,INTEGER
from sqlalchemy.orm import Mapped, mapped_column

class Menu(Base):
    __tablename__ = "menu"

    # id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    path = Column(String(50), nullable=False,comment="访问路径")

    name = Column(String(50), nullable=False, comment="路由名称")

    component = Column(String(50), nullable=False, comment="组件目录")

    redirect = Column(String(50), nullable=True, comment="路由重定向")

    meta = Column(JSON, nullable=False)

    # pid = Column(Integer, nullable=False, comment="父id")
    pid: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="父id"
    )

    updated_at = Column(DATETIME(), nullable=False)

    created_at = Column(DATETIME(), nullable=False)

    delete_time = Column(DATETIME(), nullable=True)


    # status = Column(TINYINT(1),
    #                 default=1,
    #                 nullable=False,
    #                 comment="状态 0: 禁用 1:启用")

    status: Mapped[int] = mapped_column(
        TINYINT(1),
        server_default="1",
        nullable=False,
        comment="状态 0: 禁用 1:启用"
    )

    role_ids = Column(String(255), nullable=False, comment="角色权限")

    admin_ids = Column(String(255), nullable=False, comment="单个管理员权限")


    sort = Column(Integer, nullable=False)




