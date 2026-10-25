from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class AddressBase(BaseModel):
    ciudad: str = Field(min_length=1, max_length=50)
    codigo_postal: int = Field(ge=10000, le=99999)

class AddressResponse(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

class AddressUpdate(BaseModel):
    ciudad: Optional[str] = Field(min_length=1, max_length=50)
    codigo_postal: Optional[int] = Field(ge=10000, le=99999)

class AddressCreate(AddressBase):
    user_id: int