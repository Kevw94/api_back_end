from bson import ObjectId
from fastapi import Body, Depends
from app.core.config import config
from fastapi import APIRouter
from typing import List

from app.core.security import get_current_active_user
from app.crud.crud_comments import insert_comment_in_db, try_delete_comment_in_db, try_get_comments_in_db, try_get_my_comments_in_db, try_patch_comment_in_db
from app.models.comments import CommentsModel
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post("/comments", response_description="Comment created", responses={201: {"content": {"Comment created"} }, 409: {"content": {"There were a problem with create comment try again"}}})
async def create_comment(current_user: UserModel = Depends(get_current_active_user), create_comments: CommentsModel = Body(...)):
	"""create a comment from a post with a post ID required in the body

	Args:
		current_user (UserModel, optional): get active user. Defaults to Depends(get_current_active_user).
		create_comments (CommentsModel, optional): accept string for comment. Defaults to Body(...).

	Returns:
		success: Comment created
	"""
	await insert_comment_in_db(current_user, create_comments)
	return {"success": "Comment created"}


@router.get("/comments/me", response_description="list of my commentaries", response_model=List[CommentsModel], responses={200: {"description": "list of comments of the user returned in an array" }})
async def get_my_comments(current_user: UserModel = Depends(get_current_active_user)):
	"""get all comments from the user 

	Args:
		current_user (UserModel, optional): get active user. Defaults to Depends(get_current_active_user).

	Returns:
		List[CommentsModel]: list of comments of the user returned in an array
	"""
	get_comments = await try_get_my_comments_in_db(current_user)
	return get_comments


@router.get("/comments/posts/{post_id}",  dependencies=[Depends(get_current_active_user)], response_model=List[CommentsModel],  responses={200: {"description": "list of comments related to the ID of the post" }})
async def get_comment_from_post_id(post_id: str):
	"""get comments from the posts ID

	Args:
		post_id (str): id of the post 

	Returns:
		List[CommentsModel]: list of comments related to the ID of the post
	"""
	return await try_get_comments_in_db(post_id)


@router.patch("/comments/{comments_id}", responses={201: {"content": {"Comment updated"} }, 409: {"content": {"There were a problem with update try again"}}})
async def patch_comment_by_id(comments_id: str, patch_comments: CommentsModel = Body(...), current_user: UserModel = Depends(get_current_active_user)):
	"""patch comments with the comment id and the active user

	Args:
		comments_id (str): id of the comment
		patch_comments (CommentsModel, optional): string sent in the body by the user. Defaults to Body(...).
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		success: comment updated
	"""
	await try_patch_comment_in_db(comments_id, patch_comments, current_user)
	return {"success": "Comment updated"}


@router.delete("/comments/{comments_id}", responses={201: {"content": {"Comment deleted"} }, 409: {"content": {"There were a problem with delete comment try again"}}})
async def delete_comment_by_id(comments_id: str,  current_user: UserModel = Depends(get_current_active_user)):
	"""delete comments with the comment id and the active user

	Args:
		comments_id (str): id of the comment
		current_user (UserModel, optional): active user. Defaults to Depends(get_current_active_user).

	Returns:
		success: comment updated
	"""
	await try_delete_comment_in_db(comments_id, current_user)
	return {"success": "Comment deleted"}
