from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token
from jose import JWTError
from models import User
from sqlalchemy.orm import Session
from database import SessionLocal



oauth2 = OAuth2PasswordBearer(tokenUrl="login")
# dependency function to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # closing the session no matter what

def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)  # dict with user info
        user = db.query(User).filter(User.id == payload["id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user 
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


    

    