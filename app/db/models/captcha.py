from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base
from sqlalchemy.dialects.mysql import TINYINT,DOUBLE,TEXT,INTEGER

class Captcha(Base):
    __tablename__ = "captcha"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)

    base64 = Column(TEXT, nullable=True)

    created_at = Column(DATETIME(), nullable=False)

    code = Column(String(50), nullable=True)

    expire_time = Column(Integer, nullable=True)

    use_time = Column(DATETIME(), nullable=True)



