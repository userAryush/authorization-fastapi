from fastapi import FastAPI, HTTPException, status, Depends
from database import SessionLocal, Base, engine
from models import User
from schemas import CreateUser, LoginUser
from sqlalchemy.orm import Session
from auth import hash_password, verify_password, create_access_token




app = FastAPI()
Base.metadata.create_all(engine)


# dependency function to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # closing the session no matter what


@app.post("/signup/",status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session=Depends(get_db)):
    if user.role not in ['customer','seller']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail ="Invalid Role! Choose Between seller or customer")
    
    existing_username= db.query(User).filter(User.username==user.username).first()
    existing_email = db.query(User).filter(User.email==user.email).first()
    
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    elif existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    
    return {"msg" : f"{user.role} created!", "username" : user.username, "email": user.email}

@app.post("/login/", status_code=status.HTTP_200_OK)
def log_user(user:LoginUser, db: Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email==user.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email dont exist!")
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    
    
    # create token

    token = create_access_token({"sub":existing_user.email, "role":existing_user.role, "username":existing_user.name})
    token_detail = "Add this token in the header of your request as Authorization : Bearer <token>"
    return {"msg":f"{existing_user.username}, you are logged successfully!!", "token_type": "Bearer", "token": token, "token_detail": token_detail}



        

        
    
    
    