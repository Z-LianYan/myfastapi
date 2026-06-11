from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base


class AdminLoginLog(Base):
    __tablename__ = "admin_login_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    admin_id = Column(Integer, nullable=True,comment="管理员id")

    ip = Column(String(30), nullable=True,comment="ip地址")

    login_time = Column(DATETIME(), nullable=False, comment="登录时间")


    user_agent = Column(String(255), nullable=True)
