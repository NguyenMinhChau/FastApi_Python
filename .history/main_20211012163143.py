from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello HCMUE"}
@app.get("/todo")
def read_root():
    return {"todo": "ListItem"}
@app.get("/info")
def read_root():
    return {
        "UserName": "NguyenMinhChau",
        "Password": "123456"
    }
@app.post("/hanghoa")
def read_root():
    return {
        "UserName": "NguyenMinhChau",
        "Password": "123456"
    }

# http://localhost:8000/
# http://localhost:8000/todo
# http://localhost:8000/docs
# http://localhost:8000/redoc

