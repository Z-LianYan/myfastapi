from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base
from sqlalchemy.dialects.mysql import TINYINT,DOUBLE

class AdminRole(Base):
    __tablename__ = "app_versions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    package = Column(String(225), nullable=True)

    versionCode = Column(Integer, nullable=False)

    versionName = Column(String(50), nullable=True)

    icon = Column(String(50), nullable=True)

    compileSdkVersion = Column(String(50), nullable=True)

    created_at = Column(DATETIME(), nullable=False)

    updated_at = Column(DATETIME(), nullable=False)

    platform = Column(String(50), nullable=True)

    remark = Column(String(225), nullable=True)

    status = Column(TINYINT(1),
                    default=1,
                    nullable=False,
                    comment="状态 0: 禁用 1:启用")

    delete_time = Column(DATETIME(), nullable=False)


    download_url = Column(String(225), nullable=True)

    size = Column(DOUBLE, nullable=True)

