from fastapi import FastAPI
# chỉ định các host được truy cập API
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# chỉ định các host được truy cập API này
origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}