from typing import List, Optional
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    
    username : str
    email : EmailStr
    role : str = 'customer'
    password : str
    
    model_config = {"extra" : "forbid"}
    
class LoginUser(BaseModel):
    email : EmailStr
    password : str

class CreateProduct(BaseModel):
    name:str
    price: int
    description:str
    quantity:int
    tag_ids: Optional[List[int]] = []
    # seller_id: int

class TagCreate(BaseModel):
    name: str





    

    

    
