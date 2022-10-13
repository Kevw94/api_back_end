from bson import ObjectId
from fastapi import Body, Depends
from app.core.config import config
from fastapi import APIRouter
from typing import List

from app.core.security import get_current_active_user
from app.crud.crud_comments import insert_comment_in_db, try_get_comments_in_db, try_patch_comment_in_db
from app.models.comments import CommentsModel
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post("/comments", response_description="Comment created")
async def create_comment(current_user: UserModel = Depends(get_current_active_user), create_comments: CommentsModel = Body(...)):
	await insert_comment_in_db(current_user, create_comments)
	return {"success": "Comment created"}


@router.get("/comments/posts/{post_id}",  dependencies=[Depends(get_current_active_user)], response_model=List[CommentsModel])
async def get_comment_from_post_id(post_id: str):
	return await try_get_comments_in_db(post_id)


@router.patch("/comments/{comments_id}")
async def patch_comment_by_id(comments_id: str, patch_comments: CommentsModel = Body(...), current_user: UserModel = Depends(get_current_active_user)):
	await try_patch_comment_in_db(comments_id, patch_comments, current_user)
	return {"success": "Comment updated"}