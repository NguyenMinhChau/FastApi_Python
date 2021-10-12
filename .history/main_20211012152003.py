from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "World"}
@app.get("/todo")
def read_root():
    return {"todo": "ListItem"}
