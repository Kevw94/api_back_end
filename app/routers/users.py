from http.client import HTTPException
from app.core.config import config
from fastapi import APIRouter, Depends, Body
from typing import List
from app.core.security import get_current_active_user
from app.crud.crud_users import get_all_users, try_change_password, try_check_current_password, try_change_username, try_find_user
from app.models.users import ModifPasswordModel, UserModel, UserToFrontModel
from datetime import datetime
from app.core.config import db

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/users", response_description="List of all user", response_model=List[UserToFrontModel], dependencies=[Depends(get_current_active_user)], responses={200: {"description": "List of all users with necessary information"}})
async def get_user():
	"""Get a list of all users

	Returns:
		List[UserToFrontModel]: list of all users with necessary information
	"""
	return await get_all_users()

@router.get("/users/me", response_description="return active user", response_model=UserToFrontModel, responses={200: {"description": "Information about active user"}})
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
	"""Get info about active_user

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		UserToFrontModel: return information about active user
	"""
	return current_user


@router.get("/users/{user_id}", response_description="One user by ID", response_model=UserToFrontModel, dependencies=[Depends(get_current_active_user)], responses={200: {"description": "User we get by its ID"}, 403: {"content": {"User ID doesn't exist"}}})
async def get_one_user_by_id( user_id: str):
	"""Get one user by its ID

	Args:
		user_id (str): user id we want to get

	Raises:
		HTTPException: if user doesn't exists

	Returns:
		UserToFrontModel: user we get by its ID
	"""
	user_profile_to_follow = user_id
	user_found_in_db = await try_find_user(user_profile_to_follow)
	if user_found_in_db == None: 
		raise HTTPException
	else:
		return user_found_in_db


@router.patch("/users/me", response_description="Username has been modified", dependencies=[Depends(get_current_active_user)], responses={201: {"content": {"Username has been modified"}}, 403: {"content": {"username already exists"}}, 409: {"content": {"poblem to update username in db"}}})
async def change_username_me(current_user: UserModel = Depends(get_current_active_user), modif_username: UserModel = Body(...)):
	"""Change username of the active user

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).
		modif_username (UserModel, optional): username differents or not in the Body. Defaults to Body(...).

	Returns:
		success response: username has been modified
	"""
	return await try_change_username(current_user, modif_username)


@router.patch("/users/me/password", response_description="Password of the active user has been modified", responses={201: {"content": {"Password has been changed or password incorrect"}}})
async def change_user_password(current_user: UserModel = Depends(get_current_active_user), modif_password: ModifPasswordModel = Body(...)):
	"""Change the password of the active user

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).
		modif_password (ModifPasswordModel, optional): contains current_password and new_password. Defaults to Body(...).

	Returns:
		success response: password has been changed
	"""
	is_user_checked = await try_check_current_password(current_user, modif_password)
	if is_user_checked:
		await try_change_password(is_user_checked, modif_password)
		return {"success": "password has been changed"}
	else:
		return {"error": "password is incorrect"}