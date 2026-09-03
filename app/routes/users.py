from fastapi import APIRouter, HTTPException, Query
from app.schemas.user import UserResponse, UserCreate, UserUpdate, Page
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.get("", response_model=Page[UserResponse])
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return service.list_users(page, size)

@router.post("", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate):
    return service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, changes: UserUpdate):
    user = service.update_user(user_id, changes)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}