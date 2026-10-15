from typing import Optional
from datetime import datetime
import math
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse, UserCreate, UserUpdate, Page
from app.db.database import User

class UserService:
    def list_users(self, page: int = 1, size: int = 10) -> Page[UserResponse]:
        total = len(user_db)
        pages = math.ceil(total / size)
        skip = (page - 1) * size
        items = user_db[skip:skip + size]
        return Page[UserResponse](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        for user in user_db:
            if user.id == user_id:
                return user
        return None

    def create_user(self, user: UserCreate, db: Session) -> UserResponse:
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh()
        return UserResponse.model_validate(new_user)

    def update_user(self, user_id: int, changes: UserUpdate, db: Session) -> Optional[UserResponse]:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            return None

        update_user = changes.model_dump(exclude_unset=True)
        for field, value in update_user.items():
            setattr(db_user, field, value)

        db_user.updatedAt = datetime.now()
        db.commit()
        db.refresh(db_user)

        return UserResponse.model_validate(db_user)


    def delete_user(self, user_id: int, db: Session) -> bool:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            return False

        db.delete(db_user)
        db.commit()

        return True