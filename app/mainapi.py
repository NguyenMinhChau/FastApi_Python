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

# Fix bug
@app.post("/users")
def create_user(model: MyModel.User):
    print(model)
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