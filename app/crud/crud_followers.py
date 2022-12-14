from datetime import datetime
from app.core.config import db
from bson import ObjectId
from typing import List
from app.models.followers import FollowedModel
from fastapi import HTTPException, status

from app.models.users import UserModel


async def try_insert_followers(current_user: UserModel, create_followers: FollowedModel):
	"""insert followers in db

	Args:
		current_user (UserModel): get active user
		create_followers (FollowedModel): id of the user I followed

	Raises:
		credentials_exception: There were a problem with following this user in db try again
		credentials_exception_user_not_found: The follow already exist

	Returns:
		Bool: follow has been created
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_403_FORBIDDEN,
		detail="This follow already exists or user current_user wants to follow doesn't exist",
	)
	credentials_exception_user_not_found = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with following this user try again",
	)
	created_at = datetime.now()
	is_user_followed_exists = await  db["users"].find_one({"_id": create_followers.followingId })
	is_user_followed = await db["followers"].find_one({"$and": [{"followingId": create_followers.followingId, "userId": current_user["_id"]}]})
	if is_user_followed == None and is_user_followed_exists != None:
		new_follower = {
		"userId": current_user["_id"], 
		"followingId": create_followers.followingId,
		"created_at": created_at
		}
		db["followers"].insert_one(new_follower)
		follow_created = await db["followers"].find_one({"$and": [{"followingId": create_followers.followingId, "userId": current_user["_id"], "created_at": created_at}]})
		if follow_created is not None:
			return True
		else:
			raise credentials_exception
	else:
		raise credentials_exception_user_not_found
	



async def try_get_users_following(current_user: UserModel):
	"""get posts of all users I follow

	Args:
		current_user (UserModel): get active user

	Returns:
		Array: array of articles found in db wich users I follow
	"""
	user_followed = await db["followers"].find({"userId": current_user["_id"]}).to_list(100)
	articles = []
	for i in user_followed:
		articles_users = await db["posts"].find({"userId": i["followingId"]}).to_list(100)
		for j in articles_users:
			articles.append(j)
	return articles


async def try_get_my_followers(current_user: UserModel):
	"""find in db all the followers of the current_user

	Args:
		current_user (UserModel): active user

	Returns:
		Array: return array of the followers of the current_user
	"""
	find_followers = await db["followers"].find({"followingId": current_user["_id"]}).to_list(100)
	print(find_followers)
	my_followers = []
	for i in find_followers:
		users_followed = await db["users"].find({"_id": i["followingId"]}).to_list(100)
		for j in users_followed:
			my_followers.append(j)
	return my_followers


async def try_get_my_followings(current_user: UserModel):
	"""find in db all the followings that current_user follows

	Args:
		current_user (UserModel): active user

	Returns:
		Array: array of the followings that current_user follows
	"""
	find_followings = await db["followers"].find({"userId": current_user["_id"]}).to_list(100)
	my_followings = []
	for i in find_followings:
		users_followings = await db["users"].find({"_id": i["userId"]}).to_list(100)
		for j in users_followings:
			my_followings.append(j)
	return my_followings

async def try_delete_following(follower_id: str, current_user: UserModel):
	"""delete in db a follow if current_user wants to unfollow a user

	Args:
		follower_id (str): id of the follower current_user xants to unfollow
		current_user (UserModel): active_user

	Returns:
		Bool: True if follow has been suppressed
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with deleting this follow in db try again",
	)
	await db["followers"].delete_one({"$and": [{"followingId": ObjectId(follower_id), "userId": current_user["_id"]} ]})
	follow_deleted = await db["followers"].find_one({"$and": [{"followingId": ObjectId(follower_id), "userId": current_user["_id"]} ]})
	if follow_deleted is None:
		return True
	else:
		raise credentials_exception


