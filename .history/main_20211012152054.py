from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/todo")
def read_root():
    return {"todo": "ListItem"}

# http://localhost:8000/
# http://localhost:8000/

