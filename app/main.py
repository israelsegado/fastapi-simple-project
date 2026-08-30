from pydantic import BaseModel, ConfigDict, EmailStr, ConfigDict, Field, ValidationError
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException

class Address(BaseModel):
    ciudad: str = Field(min_length=1, max_length=50)
    codigo_postal: int = Field(ge=10000, le=99999)

class UserCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    email: EmailStr
    edad: int = Field(ge=0)
    direccion: Optional[Address] = None

class UserResponse(BaseModel):
    id: int
    userCreate: UserCreate
    created_at: datetime
    updated_at: Optional[datetime] = None

users = [
    UserResponse(id=1, userCreate=UserCreate(nombre="John", email="ej@gmail.com", edad=34), created_at="2025-05-12"),
    UserResponse(id=2, userCreate=UserCreate(nombre="Jane", email="ej2@gmail.com", edad=23), created_at="2025-09-12")
    ]

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Enter a valid user"}

#función para obtener una lista de todos los usuarios
@app.get("/users")
def listUsers():
    return users

#función para crear usuarios
@app.post("/users", status_code=201, response_model=UserResponse)
def createUser(user: UserCreate):
    new_id = max(u.id for u in users) + 1
    new_user = UserResponse(id=new_id, userCreate=user, created_at=datetime.now())
    users.append(new_user)
    return new_user

#función para mostrar en pantalla el usuario con el id seleccionado
@app.get("/users/{user_id}")
def getUser(user_id: int):
    for user in users:
        if user.id == user_id:
            return {f"El usuario seleccionado es: {user}"}
        else:
            raise HTTPException(status_code=404, detail="User not found")

