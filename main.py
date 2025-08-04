from fastapi import FastAPI, HTTPException, status, Depends
from database import SessionLocal, Base, engine
from models import User, Product
from schemas import CreateUser, LoginUser, CreateProduct
from sqlalchemy.orm import Session
from auth import hash_password, verify_password, create_access_token
from dependencies import get_current_user
from sqlalchemy import and_
from dependencies import get_db
from middlewares import SimpleMiddleware, TimerMiddleware


app = FastAPI()
Base.metadata.create_all(engine)
app.add_middleware(SimpleMiddleware)
app.add_middleware(TimerMiddleware)






@app.post("/signup/",status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session=Depends(get_db)):
    if user.role not in ['customer','seller']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail ="Invalid Role! Choose Between seller or customer")
    
    existing_username= db.query(User).filter(User.username==user.username).first()
    existing_email = db.query(User).filter(User.email==user.email).first()
    
    if existing_username or existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    
    hashed_password = hash_password(user.password)
  
    user["password"] = hashed_password
    new_user = User(**user)
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

    token = create_access_token({"email":existing_user.email, "id":existing_user.id,"role":existing_user.role, "username":existing_user.username})
    token_detail = "Add this token in the header of your request as Authorization : Bearer <token>"
    return {"msg":f"{existing_user.username}, you are logged successfully!!", "token_type": "Bearer", "token": token, "token_detail": token_detail}

@app.post("/add-product/", status_code=status.HTTP_201_CREATED)
def add_product(product: CreateProduct, db:Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if current_user.role != "seller":

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only seller can add")
    
    existing_product = db.query(Product).filter(and_(Product.name==product.name , Product.seller_id == current_user.id)).first()
    if existing_product:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= f"{current_user.username} you have already added this product. If you want to add the quantity try using update endpoint!")
    
    product.seller_id = current_user.id
    
    # product["seller_id"] = current_user.id 
    # new_product = Product(name=product.name, price=product.price, quantity=product.quantity, description= product.description,seller_id=current_user.id)
    new_product = Product(**product)
    db.add(new_product)
    db.commit()
    
    return {"msg" : f"{product.name} added!", "quantity" : product.quantity, "price": product.price, "description":product.description, "supplier_username":current_user.username}





        

        
    
    
    