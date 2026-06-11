from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base


class AdminRole(Base):
    __tablename__ = "admin_role"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    role_name = Column(String(50), nullable=True)

    created_at = Column(DATETIME(), nullable=False)

    updated_at = Column(DATETIME(), nullable=False)

    remark = Column(String(255), nullable=True)

    delete_time = Column(DATETIME(), nullable=False)

    status = Column(Integer,
            default=0,
            nullable=False,
            comment="状态 0: 禁用 1:启用")


