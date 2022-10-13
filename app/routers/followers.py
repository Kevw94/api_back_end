from array import array
from http.client import HTTPException
from app.core.config import config
from fastapi import APIRouter, Depends, Body
from typing import List
from app.core.security import get_current_active_user
from app.crud.crud_followers import try_delete_following, try_get_following_id, try_get_my_followings, try_get_users_following, try_insert_followers
from app.models.followers import FollowersModel, FollowedModel
from datetime import datetime
from app.core.config import db
from app.models.posts import PostModel
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post("/followers", response_description="create follower")
async def create_follower(current_user: UserModel = Depends(get_current_active_user), create_followers: FollowedModel = Body(...)):
	response = await try_insert_followers(current_user, create_followers)
	if response == True:
		return {"success": True}
	else:
		return {"error": "sub already exists or users followed doesn't exist"}

@router.get("/posts/followers/me", response_description="list of posts I Follow users", dependencies=[Depends(get_current_active_user)], response_model=List[PostModel])
async def posts_users_me_follow(current_user: UserModel = Depends(get_current_active_user)):
	response = await try_get_users_following(current_user)
	return response

@router.get('/followers/me', response_description="list of all my followers", response_model=List[FollowersModel])
async def get_all_my_followers(current_user: UserModel = Depends(get_current_active_user)):
	response = await try_get_following_id(current_user)
	if response == None:
		return { "succes": "user doesn't have followers"}
	else: 
		return response

@router.get("/followers/following", response_description="list of all my following", response_model=List[FollowersModel])
async def get_all_my_following(current_user: UserModel = Depends(get_current_active_user)):
	response = await try_get_my_followings(current_user)
	if response is None:
		return { "succes": "user doesn't have followers"}
	else: 
		return response

@router.delete('/followers/{follower_id}', response_description="successful deleted")
async def delete_following_by_id(follower_id: str, current_user: UserModel = Depends(get_current_active_user)):
	await try_delete_following(follower_id, current_user)
	return { "success": "user has been unfollowed" }
