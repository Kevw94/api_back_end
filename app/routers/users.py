from app.core.config import config
from fastapi import APIRouter
from typing import List
from app.crud.crud_users import get_all_users
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/users", response_description="List all user", response_model=List[UserModel])
async def get_user():
	return await get_all_users()