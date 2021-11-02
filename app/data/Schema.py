from sqlalchemy import Integer,String,Column,TIMESTAMP,func,Float,ForeignKey, Boolean
from sqlalchemy.sql.schema import ForeignKey
from .Database import Base
from sqlalchemy.orm import relationship

class UserInfo(Base):
    __tablename__ ="users"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50),nullable=False)
    password = Column(String(250),nullable=False)
    active = Column(Boolean,nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())

class Category(Base):
    __tablename__ ="categories"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    categoryName = Column(String(50),nullable=False,unique=True)
    description = Column(String(255),nullable=True)
    # Tạo quan hệ giữa bảng categories và bảng products
    products = relationship("Product",back_populates="category")

class Product(Base):
    __tablename__ ="products"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String(50),nullable=False,unique=True)
    price = Column(Float,nullable=False, default=0)
    category_id = Column(Integer,ForeignKey("categories.Id"),nullable=True)
    # Tạo quan hệ giữa bảng products và bảng categories
    category = relationship("Category",back_populates="products")

