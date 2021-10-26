from sqlalchemy import Integer,String,Column,TIMESTAMP,func
from .Database import Base

class UserInfo(Base):
    __tablename__ ="users"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50),nullable=False)
    password = Column(String(250),nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())