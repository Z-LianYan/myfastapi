from sqlalchemy import Column, Integer, String, DATETIME

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), nullable=False)

    password = Column(String(100), nullable=False)

    created = Column(DATETIME(), nullable=False)