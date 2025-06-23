from fastapi import FastAPI
from app.routers.v1 import chat
import uvicorn
from app.database.in_memory_db import InMemoryDB

app = FastAPI()
app.root_path = "/api"


app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup_event():
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
