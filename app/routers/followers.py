from array import array
from http.client import HTTPException
from app.core.config import config
from fastapi import APIRouter, Depends, Body
from typing import List
from app.core.security import get_current_active_user
from app.crud.crud_followers import try_delete_following, try_get_my_followers, try_get_my_followings, try_get_users_following, try_insert_followers
from app.models.followers import FollowersModel, FollowedModel
from datetime import datetime
from app.core.config import db
from app.models.posts import PostModel
from app.models.users import UserModel, UserToFrontModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post("/followers", response_description="create follower")
async def create_follower(current_user: UserModel = Depends(get_current_active_user), create_followers: FollowedModel = Body(...)):
	"""create a follow with current_user and an other user he wants to follow

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).
		create_followers (FollowedModel, optional):Body with the id of the user current user wants to follow. Defaults to Body(...).

	Returns:
		success: follow has been created
	"""
	response = await try_insert_followers(current_user, create_followers)
	if response == True:
		return {"success": "Follow has been created"}
	else:
		return {"error": "Sub already exists or users followed doesn't exist"}


@router.get("/posts/followers/me", response_description="list of posts I Follow users", dependencies=[Depends(get_current_active_user)], response_model=List[PostModel])
async def posts_users_me_follow(current_user: UserModel = Depends(get_current_active_user)):
	"""get the posts of the followers current_user follows 

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		posts_users: return all the posts for the users current_user follows
	"""
	posts_users = await try_get_users_following(current_user)
	return posts_users


@router.get('/followers/me', response_description="list of all my followers", response_model=List[UserToFrontModel])
async def get_all_my_followers(current_user: UserModel = Depends(get_current_active_user)):
	"""get all the users that follows the current_user

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		my_followers: return all followers of the current_user
	"""
	my_followers = await try_get_my_followers(current_user)
	if my_followers == None:
		return { "succes": "user doesn't have followers"}
	else: 
		return my_followers


@router.get("/followers/following", response_description="list of all my following", response_model=List[UserToFrontModel])
async def get_all_my_following(current_user: UserModel = Depends(get_current_active_user)):
	"""get all the users that current_user is following

	Args:
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		my_followings: return all the users that current_user follows
	"""
	my_followings = await try_get_my_followings(current_user)
	if my_followings is None:
		return { "succes": "user doesn't have followers"}
	else: 
		return my_followings


@router.delete('/followers/{follower_id}', response_description="successful deleted")
async def delete_following_by_id(follower_id: str, current_user: UserModel = Depends(get_current_active_user)):
	"""delete follow if current_user wants to unfollow a user

	Args:
		follower_id (str): id of the user current_user wants to unfollow
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		success: user has been unfollowed
	"""
	await try_delete_following(follower_id, current_user)
	return { "success": "user has been unfollowed" }
