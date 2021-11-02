from fastapi import FastAPI
from .data import Schema
from .data.Database import engine,MySessions
from .Models import MyModel

app = FastAPI(
    title="My FastAPI",
    description="Demo FastAPI + SQL Alchemy ORM MySQL",
    version="1.0.0"
)

#Định nghĩa Schema cho database
Schema.Base.metadata.create_all(bind=engine)

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


@app.get("/category")
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


@app.get("/prducts")
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