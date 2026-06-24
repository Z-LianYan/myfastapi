from sqlalchemy import Column, Integer, String, DATETIME, text

from app.db.base import Base
from sqlalchemy.dialects.mysql import TINYINT,INTEGER
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel,ConfigDict
from datetime import datetime

class AdminRole(Base):
    __tablename__ = "admin_role"

    # id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)
    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        index=True,
        autoincrement=True
    )

    role_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="角色名称"
    )

    # created_at = Column(DATETIME(), nullable=False)
    created_at: Mapped[str] = mapped_column(
        DATETIME(),
        nullable=False,
        comment=""
    )

    # updated_at = Column(DATETIME(), nullable=False)
    updated_at: Mapped[str] = mapped_column(
        DATETIME(),
        nullable=False,
        comment=""
    )

    remark: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="备注"
    )

    delete_time: Mapped[str] = mapped_column(
        DATETIME(),
        nullable=True,
        comment=""
    )

    # status = Column(Integer,
    #         server_default=text("0"),
    #         nullable=False,
    #         comment="状态 0: 禁用 1:启用")

    status: Mapped[int] = mapped_column(
        TINYINT(1),
        server_default="1",
        nullable=False,
        comment="状态 0: 禁用 1:启用"
    )



class AdminRoleVO(BaseModel):
    id: int
    role_name: str
    status: int
    remark: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    delete_time: datetime | None = None

    # model_config = {
    #     "from_attributes": True,
    #     "ser_json_timedelta": 'iso8601',  # 例子
    # }

    model_config = ConfigDict(
        from_attributes=True,
        ser_json_timedelta='iso8601',  # 例子
    )