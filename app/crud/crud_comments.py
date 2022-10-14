from datetime import datetime
from app.core.config import db
from bson import ObjectId
from typing import List
from app.models.comments import CommentsModel
from app.models.followers import FollowedModel
from pymongo import ReturnDocument
from fastapi import HTTPException, status

from app.models.users import UserModel


async def insert_comment_in_db(current_user: UserModel, create_comments: CommentsModel):
	"""create comment and insert it in the DB

	Args:
		current_user (UserModel): active user 
		create_comments (CommentsModel): create_comment coming's from the body request
	
	Raises:
		HTTPException: 409 if problem to insert new comment in the DB

	Returns:
		Bool: return true if insert good
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with create comment try again",
	)
	created_at = datetime.now()
	comment = {
		"postId": create_comments.postId,
		"userId": current_user["_id"],
		"content": create_comments.content,
		"created_at": created_at

	}
	await db["comments"].insert_one(comment)
	comment_inserted = await db["comments"].find_one({"$and": [{"postId": create_comments.postId, "userId": current_user["_id"], "content": create_comments.content, "created_at": created_at}]})
	if comment_inserted is not None:
		return True
	else:
		raise credentials_exception



async def try_get_comments_in_db(post_id: str):
	"""get comments from the db with the post id 

	Args:
		post_id (str): post id from the path parameters

	Returns:
		List[CommentsModel]: list of comments 
	"""
	comments = await db["comments"].find({"postId": ObjectId(post_id)}).to_list(100)
	return comments


async def try_patch_comment_in_db(comments_id: str, patch_comments: CommentsModel, current_user: UserModel):
	"""patch comment in the db with comment ID and active_user ID

	Args:
		comments_id (str): comment ID
		patch_comments (CommentsModel): comment modified and get in the body of request
		current_user (UserModel): active user

	Raises:
		HTTPException: 409 if problem to update comment in the DB

	Returns:
		Bool: success comment patched
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with update try again",
	)
	await db["comments"].update_one(
		{
			"$and": 
				[
					{
						"_id": ObjectId(comments_id),
						"userId": current_user["_id"]
					}
				]
		},
		{
			"$set": 
				{
					"content": patch_comments.content
				}
		})
	comment_updated = await db["comments"].find_one({"$and": [{"_id": ObjectId(comments_id), "userId": current_user["_id"], "content": patch_comments.content}]})
	if comment_updated is not None:
		return True
	else:
		raise credentials_exception


async def try_get_my_comments_in_db(current_user: UserModel):
	"""get all comments of the user

	Args:
		current_user (UserModel): active user

	Returns:
		List[CommentsModel]: list of comments from the user 
	"""
	comments = await db["comments"].find({"userId": ObjectId(current_user["_id"])}).to_list(100)
	return comments


async def try_delete_comment_in_db(comments_id: str, current_user: UserModel):
	"""delete comment in db with its id and user Id

	Args:
		comments_id (str): id of the comment
		current_user (UserModel): active user
	
	Raises:
		HTTPException: 409 if problem to delete comment in the DB

	Returns:
		Bool: Success deleted
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with delete comment try again",
	)
	await db["comments"].delete_one({
		"$and": 
				[
					{
						"_id": ObjectId(comments_id),
						"userId": current_user["_id"]
					}
				]
	})
	comment_deleted = await db["comments"].find_one({"$and": [{"_id": ObjectId(comments_id), "userId": current_user["_id"]}]})
	if comment_deleted is None:
		return True
	else:
		raise credentials_exception