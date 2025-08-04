# hash_password
# verify
# create_token
# decode_token
from jose import jwt 
from passlib.context import CryptContext
from datetime import datetime,timezone, timedelta
from config import Settings 

pwd_context = CryptContext(schemes="bcrypt", deprecated ="auto")

setting = Settings()
SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
TOKEN_EXPIRY_TIME_MINUTES = setting.TOKEN_EXPIRY_TIME_MINUTES

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

