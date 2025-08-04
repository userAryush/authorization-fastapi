from database import Base
from sqlalchemy import Integer, String, Column


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200))
    role = Column(String(50), default="customer")
    
    

    

    