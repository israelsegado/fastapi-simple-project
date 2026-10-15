from fastapi import FastAPI
from contextlib import contextmanager

from app.routes import users
from app.db.database import init_db


@contextmanager
def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Enter a valid user"}