from pydantic import BaseModel, EmailStr, ConfigDict, Field, ValidationError, field_validator, model_validator, BeforeValidator
from typing import Optional, Annotated, Generic, TypeVar, List
from datetime import datetime
import re

class Address(BaseModel):
    ciudad: str = Field(min_length=1, max_length=50)
    codigo_postal: int = Field(ge=10000, le=99999)

def normalize_phone(value: str) -> str:
    digits = re.sub(r'\D', '', value)
    if len(digits) == 9:
        return f"+34{digits}"
    elif len(digits) == 11 and digits.startswith('34'):
        return f"+{digits}"
    else:
        raise ValueError('Phone must be 9 digits, or 11 starting with 34')

PhoneNumber = Annotated[str, BeforeValidator(normalize_phone)]

class UserBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    email: EmailStr
    edad: int = Field(ge=18)
    direccion: Optional[Address] = None
    telefono: Optional[PhoneNumber] = None

    @field_validator('email', mode='before')
    @classmethod
    def validateEmail(cls, mail: EmailStr):
        return mail.strip().lower()

json_example = {
    "example": {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "edad": 30,
        "direccion": {
            "ciudad": "Madrid",
            "codigo_postal": 28001
        },
        "telefono": "618302964",
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

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int