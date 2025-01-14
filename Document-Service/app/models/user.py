from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__="user"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True, index=True, nullable=False)
    email=Column(String, unique=True, nullable=False)
    hash_password=Column(String, nullable=False)
