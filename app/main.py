from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import users
from app.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()      # sync function, no await needed
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Enter a valid user"}