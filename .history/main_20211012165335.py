from fastapi import FastAPI
# tạo file __init__.py để gợi ý import trong models
from .models.Mymodel import HangHoa

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
async def them_hang_hoa(model: HangHoa):
    print(model)
    return {
        "UserName": "NguyenMinhChau",
        "Password": "123456"
    }

# http://localhost:8000/
# http://localhost:8000/todo
# http://localhost:8000/docs
# http://localhost:8000/redoc

