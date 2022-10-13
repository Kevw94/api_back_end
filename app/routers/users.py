from http.client import HTTPException
from app.core.config import config
from fastapi import APIRouter, Depends, Body
from typing import List
from app.core.security import get_current_active_user
from app.crud.crud_users import get_all_users, try_change_password, try_check_current_password, try_change_username, try_find_user
from app.models.users import ModifPasswordModel, UserModel
from datetime import datetime
from app.core.config import db

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/users", response_description="List all user", response_model=List[UserModel])
async def get_user():
	return await get_all_users()

@router.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
	return { "id": current_user["_id"], "username": current_user["username"]}


@router.get("/users/{user_id}", response_description="One user", response_model=UserModel, dependencies=[Depends(get_current_active_user)])
async def get_one_user_by_id( user_id: str):
	user_profile_to_follow = user_id
	user_found_in_db = await try_find_user(user_profile_to_follow)
	if user_found_in_db == None: 
		raise HTTPException
	else:
		return {
			"id": user_found_in_db["_id"],
			"username": user_found_in_db["username"],
			"created_at": user_found_in_db["created_at"]
		}


@router.patch("/users/me", dependencies=[Depends(get_current_active_user)])
async def change_username_me(current_user: UserModel = Depends(get_current_active_user), modif_username: UserModel = Body(...)):
	return await try_change_username(current_user, modif_username)


@router.patch("/users/me/password")
async def change_user_password(current_user: UserModel = Depends(get_current_active_user), modif_password: ModifPasswordModel = Body(...)):
	is_user_checked = await try_check_current_password(current_user, modif_password)
	if is_user_checked:
		await try_change_password(is_user_checked, modif_password)
		return True
	else:
		return {"error": "password is incorrect"}