import math
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.address import Page, AddressResponse, AddressCreate, AddressUpdate
from app.db.database import Address, User

class AddressService:
    def list_addresses(self, db: Session, page: int = 1, size: int = 10) -> Page[AddressResponse]:
        total = db.query(func.count(Address.id)).scalar()
        pages = math.ceil(total / size)
        skip = (page - 1) * size

        address = db.query(Address).offset(skip).limit(size).all()
        items = [AddressResponse.model_validate(u) for u in address]

        return Page[AddressResponse](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    def get_address(self, db: Session, address_id: int) -> Optional[AddressResponse]:
        db_address = db.query(Address).where(Address.id == address_id).first()

        if not db_address:
            return None

        return AddressResponse.model_validate(db_address)

    def create_address(self, db: Session, address: AddressCreate) -> Optional[AddressResponse]:
        db_user = db.query(User).where(User.id == address.user_id).first()

        if not db_user:
            return None

        new_address = Address(**address.model_dump())

        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        return AddressResponse.model_validate(new_address)

    def update_address(self, db: Session, changes: AddressUpdate, address_id: int) -> Optional[AddressResponse]:
        db_address = db.query(Address).where(Address.id == address_id).first()

        if not db_address:
            return None

        update_address = changes.model_dump(exclude_unset=True)
        for field, value in update_address.items():
            if value is not None:
                setattr(db_address, field, value)

        db.commit()
        db.refresh(db_address)

        return AddressResponse.model_validate(db_address)

    def delete_address(self, db: Session, address_id: int) -> bool:
        db_address = db.query(Address).where(Address.id == address_id).first()

        if not db_address:
            return False

        db.delete(db_address)
        db.commit()

        return True