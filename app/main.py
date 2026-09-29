# uvicorn app.main:app --host 127.0.0.1 --port 9090 --reload
import sys
sys.dont_write_bytecode = True

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.models.db import init_db
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router

@asynccontextmanager
async def lifespan(_app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# CORS: browsers block a page on one origin (the React app, http://localhost:5173)
# from reading responses from another origin (this API, port 9090) unless the
# API explicitly allows it with these headers.
app.add_middleware(
    CORSMiddleware,
    # Only our own frontend(s). Never "*" together with allow_credentials=True.
    allow_origins=CORS_ORIGINS,
    # Lets the browser send and receive cookies (our refresh_token cookie)
    # on cross-origin requests. The React side must also use credentials: "include".
    allow_credentials=True,
    allow_methods=["*"],
    # Needed so React can send "Authorization: Bearer <token>" and JSON bodies.
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/")
def welcome():
    return "Welcome to server"

app.include_router(user_router)
# Registers POST /auth/login, which issues JWT tokens used by the protected user routes.
app.include_router(auth_router)


# npx create-react-router@latest todo-fastapi-client