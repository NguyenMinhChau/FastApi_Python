import uvicorn
if __name__ == "__main__":
    # reload=True => lắng nghe sự thay đổi của file main.py
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
