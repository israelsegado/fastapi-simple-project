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

    def update_user(self, user_id: int, changes: UserUpdate) -> Optional[UserResponse]:
        for i, user in enumerate(user_db):
            if user.id == user_id:
                update_data = changes.model_dump(exclude_defaults=True)
                user_data = user.model_dump()
                user_data.update(update_data)
                user_data["updated_at"] = datetime.now()

                updated_user = UserResponse(**user_data)
                user_db[i] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: int) -> bool:
        for i, user in enumerate(user_db):
            if user.id == user_id:
                del user_db[i]
                return True
        return False