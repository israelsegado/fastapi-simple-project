from pydantic import BaseModel, EmailStr, ConfigDict, Field, ValidationError
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException

class Address(BaseModel):
    ciudad: str = Field(min_length=1, max_length=50)
    codigo_postal: int = Field(ge=10000, le=99999)

class UserBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    email: EmailStr
    edad: int = Field(ge=18)
    direccion: Optional[Address] = None

class UserResponse(BaseModel):
    id: int
    userCreate: UserBase
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    nombre: str = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    edad: Optional[int] = Field(None, ge=18)
    direccion: Optional[Address] = None


user_db: list[UserResponse] =[
    UserResponse(id=1, userCreate=UserBase(nombre="John", email="ej@gmail.com", edad=34), created_at="2025-05-12"),
    UserResponse(id=2, userCreate=UserBase(nombre="Jane", email="ej2@gmail.com", edad=23), created_at="2025-09-12")
    ]

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Enter a valid user"}

#función para obtener una lista de todos los usuarios
@app.get("/users")
def listUsers():
    return user_db

#función para crear usuarios
@app.post("/users", status_code=201, response_model=UserResponse)
def createUser(user: UserBase):
    new_id = max(u.id for u in user_db) + 1
    new_user = UserResponse(id=new_id, userCreate=user, created_at=datetime.now())
    user_db.append(new_user)
    return new_user

#función para mostrar en pantalla el usuario con el id seleccionado
@app.get("/users/{user_id}")
def getUser(user_id: int):
    for user in user_db:
        if user.id == user_id:
            return {"user": user}

    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=UserResponse)
def updateUser(user_idx: int, changes: UserUpdate):
    for user in user_db:
        if user.id == user_idx:
            data = user.model_dump()
            if changes.nombre is not None:
                data["nombre"] = changes.nombre
            update = UserResponse(**data)
            user_db.append(update)
            return data

    raise HTTPException(status_code=404, detail="User not found")