from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings

class CreateUser(BaseModel):
    
    username : str
    email : EmailStr
    role : str = 'customer'
    password : str
    
class LoginUser(BaseModel):
    email : EmailStr
    password : str
    
class Setting(BaseSettings):
    
    SECRET_KEY :str
    ALGORITHM : str 
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    
    model_config = {"env_file" : ".env"}
    

    
