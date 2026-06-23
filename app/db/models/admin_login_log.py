from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base

from sqlalchemy.dialects.mysql import TINYINT,INTEGER
from sqlalchemy.orm import Mapped, mapped_column

class AdminLoginLog(Base):
    __tablename__ = "admin_login_log"

    # id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    admin_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="管理员id"
    )

    ip: Mapped[int] = mapped_column(
        String(30),
        nullable=True,
        comment="ip地址"
    )

    login_time: Mapped[str] = mapped_column(
        DATETIME(),
        nullable=False,
        comment="登录时间"
    )

    user_agent: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment=""
    )
