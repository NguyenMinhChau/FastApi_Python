from fastapi import FastAPI
from .models import 
app = FastAPI()
@app.get("/")
async def read_root():
    return {"message": "Hello HCMUE"}
@app.get("/todo")
async def read_root():
    return {"todo": "ListItem"}
@app.get("/info")
async def read_root():
    return {
        "UserName": "NguyenMinhChau",
        "Password": "123456"
    }
#snake_case
@app.post("/hanghoa")
async def them_hang_hoa():
    return {
        "UserName": "NguyenMinhChau",
        "Password": "123456"
    }

# http://localhost:8000/
# http://localhost:8000/todo
# http://localhost:8000/docs
# http://localhost:8000/redoc

