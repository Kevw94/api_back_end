from app.core.config import config
from fastapi import APIRouter, Depends
from typing import List
from app.core.security import get_current_active_user
from app.crud.crud_users import get_all_users
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/users", response_description="List all user", response_model=List[UserModel])
async def get_user():
	return await get_all_users()

@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
	return current_user