from pydantic_settings import BaseSettings


        
class Settings(BaseSettings):
    
    SECRET_KEY :str
    ALGORITHM : str 
    TOKEN_EXPIRY_TIME_MINUTES : int
    DATABASE_URL : str
    
    model_config = {"env_file" : ".env"}
    

    

    
