from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base
from sqlalchemy.dialects.mysql import TINYINT,DOUBLE,INTEGER


class AdminVersions(Base):
    __tablename__ = "app_versions"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)

    package = Column(String(225), nullable=True, comment="安装包名")

    versionCode = Column(Integer, nullable=False)

    versionName = Column(String(50), nullable=True, comment="app版本")

    icon = Column(String(50), nullable=True, comment="app图标")

    compileSdkVersion = Column(String(50), nullable=True, comment="编译sdk版本")

    created_at = Column(DATETIME(), nullable=False)

    updated_at = Column(DATETIME(), nullable=False)

    platform = Column(String(50), nullable=True, comment="平台 android, ios")

    remark = Column(String(225), nullable=True, comment="更新备注")

    status = Column(TINYINT(1),
                    default=1,
                    nullable=False,
                    comment="状态 0: 禁用 1:启用")

    download_url = Column(String(225), nullable=True,comment="下载地址")

    size = Column(DOUBLE, nullable=True,comment="安装包大小")

