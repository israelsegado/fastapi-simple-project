# print("EJERCICIO 1:\n")

# from pydantic import BaseModel, ConfigDict, EmailStr, ConfigDict, Field, ValidationError
# from typing import Optional

# class Address(BaseModel):
#     model_config = ConfigDict(frozen=True, extra="ignore")
#     ciudad: str
#     codigo_postal: int = Field(ge=10000, le=99999)

# class User(BaseModel):
#     model_config = ConfigDict(extra='forbid', str_strip_whitespace=True, frozen=True)

#     email: EmailStr
#     edad: int = Field(gt=18)
#     nombre: str = Field(min_length=2)
#     direccion: Optional[Address] = None

# inf_ok = {"email": "ejemplo@gmail.com", "edad": 20, "nombre": "John"}
# inf_bad = {"email": "jane", "edad": 15, "nombre": "Jane"}

# user1 = User(email="ejemplo@gmail.com", edad=20, nombre="   John   ")
# print(f"Nombre sin espacios: {user1.nombre}\n")

# # Bloque errores de validación de datos de entrada -------------------
# try:
#     print("Probando a hacer las validaciones de datos de entrada válidos")
#     User.model_validate(inf_ok)
#     User.model_validate(inf_bad)
    

# except ValidationError as exc:
#     for e in exc.errors():
#         print(f"Campo: {e['loc']}")      
#         print(f"Mensaje: {e['msg']}")
#         print(f"Tipo: {e['type']}")      
#         print(f"Input: {e['input']}")     
#         print("---")
# #---------------------------------------------------------

# # Bloque prueba del atributo frozen ----------------------
# try:
#     print("\nProbando a hacer cambios en una clase con atributo frozen")
#     user1.nombre = "Jane"

# except ValidationError as exc:
#     for e in exc.errors():
#         print(f"Campo: {e['loc']}")      
#         print(f"Mensaje: {e['msg']}")
#         print(f"Tipo: {e['type']}")      
#         print(f"Input: {e['input']}")     
#         print("---")
# #-----------------------------------------------------

# print(f'{'='*100}')

print("EJERCICIO 2:\n")

from pydantic import BaseModel, ConfigDict, EmailStr, ConfigDict, Field, ValidationError
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException

class Address(BaseModel):
    ciudad: str
    codigo_postal: int

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    edad: int
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
@app.post("/users")
def createUser(user: UserCreate):
    return user

#función para mostrar en pantalla el usuario con el id seleccionado
@app.get("/users/{user_id}")
def getUser(user_id: int):
    for user in users:
        if user.id == user_id:
            return {f"El usuario seleccionado es: {user}"}
        else:
            raise HTTPException(status_code=404, detail="User not found")

