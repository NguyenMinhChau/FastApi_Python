from fastapi import FastAPI
# chỉ định các host được truy cập API
from fastapi.middleware.cors import CORSMiddleware
# dùng file json
import json
# pathLib vì open


app = FastAPI()

# chỉ định các host được truy cập API này
origins = [
    "http://localhost:3000",
    "localhost:3000"
]
todos = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    }
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
    with open('app/db.json',"r") as the_file:
        data = the_file.read()
        print(data)
    # data = json.load()
    return { "data": todos }

# Run: python backend\main.py