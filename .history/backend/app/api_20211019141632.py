from fastapi import FastAPI, UploadFile, File
# chỉ định các host được truy cập API
from fastapi.middleware.cors import CORSMiddleware
# dùng file json
import json
# pathLib vì open db.json -> Error
from pathlib import Path
import os
from .models.Todo import TodoItem
import logging
#LOG: Thứ tự debug(), info(), warning(), error(), and critical()

#Cách 1
#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
#Cách 2: Lưu xuống file.log
logger = logging.getLogger()
f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

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
    logging.error("This is error")
    return {"message": "Welcome to your todo list."}


@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    folder = Path(__file__).parent
    my_path_file = os.path.join(folder,"db.json")
    with open(my_path_file,"r") as the_file:
        data = the_file.read()
    data = json.loads(data)
    return { "data": data }


folder = Path(__file__).parent
my_path_file = os.path.join(folder,"db.json")

def read_todo_data():
    try:
        with open(my_path_file,"r") as the_file:
            data = the_file.read()
        return json.loads(data)
    except Exception as e:
        logging.error(e)

@app.post("/upload")
def upload_single_file(file: UploadFile = f):

@app.post("/todo", tags=["todos"])
async def add_todo(todo: TodoItem) -> dict:
    data = read_todo_data()
    # Kiểu list nên dùng append
    data.append({
        'id': todo.id,
        'item': todo.item,
    })
    # Save
    with open(my_path_file,"w") as the_file:
        # the_file.write(json.dumps(data))
        json.dump(data, the_file, indent=4)
    return {
        "data": { "Todo added." }
    }

@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: TodoItem) -> dict:
    data = read_todo_data()
    for todo in data:
        if int(todo["id"]) == id:
            todo["item"] = body.item
            with open(my_path_file,"w") as the_file:
                # the_file.write(json.dumps(data))
                json.dump(data, the_file, indent=4)
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    data = read_todo_data()
    for todo in data:
        if int(todo["id"]) == id:
            data.remove(todo)
            with open(my_path_file,"w") as the_file:
                # the_file.write(json.dumps(data))
                json.dump(data, the_file, indent=4)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }


@app.get("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    data = read_todo_data()
    for todo in data:
        if int(todo["id"]) == id:
            return todo
    return {
        "data": f"Todo with id {id} not found."
    }
# Run: python backend\main.py