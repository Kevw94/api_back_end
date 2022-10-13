from http.client import HTTPException
from app.core.config import config
from fastapi import APIRouter, Depends, Body
from typing import List
from app.core.security import get_current_active_user
from app.crud.crud_followers import try_insert_followers
from app.models.followers import FollowersModel, FollowedModel
from datetime import datetime
from app.core.config import db
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