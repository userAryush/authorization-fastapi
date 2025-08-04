from database import Base
from sqlalchemy import Integer, String, Column, Float,ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200))
    role = Column(String(50), default="customer")
    
    products = relationship("Product", back_populates="seller")
    

    
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String(200),  index=True)
    price = Column(Float, index= True)
    quantity = Column(Integer)
    description = Column(String(500), index=True)
    
    seller_id = Column(Integer, ForeignKey("users.id"))  
    seller = relationship("User", back_populates="products")  

    
    
    

    

    