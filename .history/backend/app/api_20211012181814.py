from fastapi import FastAPI
# chỉ định các host được truy cập API
from fastapi.middleware.cors import CORSMiddleware
# dùng file json
import json
# pathLib vì open db.json -> Error
from pathlib import Path
import os
from .models.

app = FastAPI()

# chỉ định các host được truy cập API này
origins = [
    "http://localhost:3000",
    "localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    # Cho tất cả các host
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    folder = Path(__file__).parent
    my_path_file = os.path.join(folder,"db.json")
    with open(my_path_file,"r") as the_file:
        data = the_file.read()
        print(data)
    data = json.loads(data)
    print(type(data))
    return { "data": data }

@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    print(todo)
    return {
        "data": { "Todo added." }
    }
# Run: python backend\main.py