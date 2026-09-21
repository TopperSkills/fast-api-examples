# uvicorn app.main:app --host 127.0.0.1 --port 9090 --reload
import sys
sys.dont_write_bytecode = True

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.db import init_db
from app.routers.user_router import router as user_router

@asynccontextmanager
async def lifespan(_app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
@app.get("/")
def welcome():
    return "Welcome to server"

app.include_router(user_router)