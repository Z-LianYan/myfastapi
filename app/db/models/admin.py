from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base

from sqlalchemy.dialects.mysql import TINYINT

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    phone = Column(String(50), nullable=True)

    name = Column(String(100), nullable=True)

    password = Column(String(100), nullable=True)

    created_at = Column(DATETIME(), nullable=False)

    updated_at = Column(DATETIME(), nullable=False)

    role_id = Column(Integer, nullable=False, comment="角色id")

    last_login_time = Column(DATETIME(), nullable=False)

    status = Column(TINYINT(1),
            default=1,
            nullable=False,
            comment="状态 0: 禁用 1:启用")

    delete_time = Column(DATETIME(), nullable=False)

    avatar = Column(String, nullable=True, comment="头像")

