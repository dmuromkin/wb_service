from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api import abc
from src.database import engine, init_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield
    await engine.dispose()

app = FastAPI(
    title="WB Test API", 
    version="1.0.0",
    lifespan=lifespan
)

allowed_origins = [
    "http://localhost:5173",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],            
)


app.include_router(abc.router) 