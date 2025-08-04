from database import Base
from sqlalchemy import Integer, String, Column, Float,ForeignKey, Table
from sqlalchemy.orm import relationship


# product_tag_link = Table('product_tag', Base.metadata,
#                          Column('product_id', Integer, ForeignKey('product.id')),
#                          Column('tag_id', Integer, ForeignKey('tags.id')))

class ProductTag(Base):
    __tablename__ = 'product_tag'
    id = Column(Integer, primary_key=True)
    student_id = Column('product_id', Integer, ForeignKey('products.id'))
    course_id = Column('tag_id', Integer, ForeignKey('tags.id'))
    
    
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
    
    tags = relationship("Tag", secondary = "product_tag")

    
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    products = relationship("Product", secondary = "product_tag")
    
    
    

    

    