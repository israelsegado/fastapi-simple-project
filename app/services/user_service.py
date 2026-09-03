from typing import Optional
from datetime import datetime
import math

from app.schemas.user import UserResponse, UserCreate, UserUpdate, Page

user_db: list[UserResponse] = [
    UserResponse(id=1, nombre="John", email="ej@gmail.com", edad=34, telefono="618302984", created_at=datetime(2025,5,12), updated_at=None),
    UserResponse(id=2, nombre="Jane", email="ej2@gmail.com", edad=23, created_at=datetime(2025,9,12), updated_at=None)
]

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

    def create_user(self, user: UserCreate) -> UserResponse:
        new_user = UserResponse(
            id=max(u.id for u in user_db) + 1,
            **user.model_dump(),
            created_at=datetime.now(),
            updated_at=None
        )
        user_db.append(new_user)
        return new_user

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