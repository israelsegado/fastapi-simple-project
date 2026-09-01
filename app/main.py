from pydantic import BaseModel, EmailStr, ConfigDict, Field, ValidationError, field_validator, model_validator
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

    @field_validator('email', mode='before')
    @classmethod
    def validateEmail(cls, mail: EmailStr):
        return mail.strip().lower()

json_example= {
    "example": {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "edad": 30,
        "direccion": {
            "ciudad": "Madrid",
            "codigo_postal": 28001
            },
        "created_at": "2026-01-15T10:30:00Z",
        "updated_at": "2026-01-15T12:45:00Z"
        }
    }

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_schema_extra=json_example)

    id: int
    created_at: datetime = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class UserCreate(UserBase):
    @model_validator(mode='after')
    def validateAddress(self):
        if self.direccion:
            if self.direccion.ciudad is not None and self.direccion.codigo_postal is not None:
                return self
            elif (self.direccion.ciudad is None and self.direccion.codigo_postal is not None) or (self.direccion.ciudad is not None and self.direccion.codigo_postal is None):
                raise ValueError("You must write both city and postal code.")
            else:
                return self
        else:
            return self

class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    edad: Optional[int] = Field(None, ge=18)
    direccion: Optional[Address] = None

class UserDB(UserBase):
    pass


user_db: list[UserResponse] = [
    UserResponse(id=1, nombre="John", email="ej@gmail.com", edad=34, created_at=datetime(2025,5,12), updated_at=None),
    UserResponse(id=2, nombre="Jane", email="ej2@gmail.com", edad=23, created_at=datetime(2025,9,12), updated_at=None)
]

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Enter a valid user"}

# función para obtener una lista de todos los usuarios
@app.get("/users")
def listUsers():
    return user_db

# función para crear usuarios
@app.post("/users", status_code=201, response_model=UserResponse)
def createUser(user: UserCreate):
    new_user = UserResponse(
        id=max(u.id for u in user_db) + 1,
        **user.model_dump(),
        created_at=datetime.now(),
        updated_at=None
    )
    user_db.append(new_user)
    return new_user

# función para mostrar en pantalla el usuario con el id seleccionado
@app.get("/users/{user_id}")
def getUser(user_id: int):
    for user in user_db:
        if user.id == user_id:
            return {"user": user}

    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=UserResponse)
def updateUser(user_id: int, changes: UserUpdate):
    for i, user in enumerate(user_db):
        if user.id == user_id:
            update_data = changes.model_dump(exclude_defaults=True)
            user_data = user.model_dump()
            user_data.update(update_data)
            user_data["updated_at"] = datetime.now()

            updated_user = UserResponse(**user_data)
            user_db[i] = updated_user

            return updated_user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def deleteUser(user_id: int):
    for i, user in enumerate(user_db):
        if user.id == user_id:
            del user_db[i]
            return {"message": "User deleted"}
            
    raise HTTPException(status_code=404, detail="User not found")