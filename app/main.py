from fastapi import FastAPI
from app.routes import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Enter a valid user"}