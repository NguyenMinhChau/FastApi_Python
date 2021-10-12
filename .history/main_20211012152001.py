from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"mess": "World"}
@app.get("/todo")
def read_root():
    return {"todo": "ListItem"}

