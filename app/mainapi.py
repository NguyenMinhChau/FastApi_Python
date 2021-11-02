from fastapi import FastAPI,HTTPException, status,Depends
from datetime import datetime, timedelta
from .data import Schema
from .data.Database import engine,MySessions
from .Models import MyModel
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(
    title="My FastAPI",
    description="Demo FastAPI + SQL Alchemy ORM MySQL",
    version="1.0.0"
)

#Định nghĩa Schema cho database
Schema.Base.metadata.create_all(bind=engine)

# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    session = MySessions()
    return session.query(Schema.UserInfo).filter(Schema.UserInfo.username == username).one_or_none()

def authenticate_user(model: MyModel.User):
    user = get_user(model.username)
    if not user:
        return False
    # if not verify_password(model.password, user.hashed_password):
    #     return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = MyModel.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Schema.UserInfo = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/authenticate")
def authenticate(model: MyModel.User):
    user = authenticate_user(model)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def home():
    return {"message": "Hello" }

@app.get("/users")
def get_all_user():
    session = MySessions()
    users = session.query(Schema.UserInfo).all()
    items = []
    for item in users:
        items.append({
            "username": item.username,
            "password": item.password,
        })
    return {"data": items}


@app.get("/category",tags=["CATEGORY"])
def get_all_category():
    session = MySessions()
    categorys = session.query(Schema.Category).all()
    items = []
    for item in categorys:
        items.append({
            "id": item.Id,
            "name": item.categoryName,
            "product": item.products
        })
    return {"data": items}

@app.post("/category",tags=["CATEGORY"])
def create_new_category(model: MyModel.CategoryModel, current_user: Schema.UserInfo = Depends(get_current_active_user)):
    print(current_user)
    session = MySessions()
    new_cate = Schema.Category(
        categoryName=model.name,
        description=model.desc,
    )
    session.add(new_cate)
    session.commit()
    session.refresh(new_cate)
    return {"data": new_cate}

@app.get("/products")
def get_all_products():
    session = MySessions()
    products = session.query(Schema.Product).all()
    items = []
    for item in products:
        items.append({
            "id": item.Id,
            "name": item.productName,
            "category": item.category
        })
    return {"data": items}


@app.get("/prducts/query")
def get_all_products(price_from: float, price_to: float):
    session = MySessions()
    products = session.query(Schema.Product).filter(Schema.Product.price >= price_from).filter(Schema.Product.price <= price_to).all()
    items = []
    for item in products:
        items.append({
            "id": item.Id,
            "name": item.productName,
            "category": item.category
        })
    return {"data": items}

# Fix bug
@app.post("/users")
def create_user(model: MyModel.User):
    myuser = Schema.UserInfo
    myuser.username = model.username
    myuser.password = model.password
    session = MySessions()
    try:
        session.add(myuser)
        session.commit()
        session.refresh(myuser)
    finally:
        session.close()
    return {"data": myuser}