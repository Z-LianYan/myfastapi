from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

from sqlalchemy.dialects.mysql import TINYINT,INTEGER

class Admin(Base):
    __tablename__ = "admin"

    # id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    # phone = Column(String(50), nullable=False, comment="手机号")

    phone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="手机号码"
    )

    name = Column(String(100), nullable=False, comment="姓名")

    password = Column(String(100), nullable=False, comment="账号密码")

    created_at = Column(DATETIME(), nullable=False)

    updated_at = Column(DATETIME(), nullable=False)

    role_id = Column(Integer, nullable=True, comment="角色id")

    last_login_time = Column(DATETIME(), nullable=True)

    status = Column(TINYINT(1),
            default=1,
            nullable=False,
            comment="状态 0: 禁用 1:启用")

    delete_time = Column(DATETIME(), nullable=True)

    avatar = Column(String(255), nullable=True, comment="头像")


