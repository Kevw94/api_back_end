from datetime import datetime
from app.core.config import db
from bson import ObjectId
from typing import List
from app.models.comments import CommentsModel
from app.models.followers import FollowedModel

from app.models.users import UserModel


async def insert_comment_in_db(current_user: UserModel, create_comments: CommentsModel):
	created_at = datetime.now()
	comment = {
		"postId": create_comments.postId,
		"userId": current_user["_id"],
		"content": create_comments.content,
		"created_at": created_at

	}
	await db["comments"].insert_one(comment)
	return True


async def try_get_comments_in_db(post_id: str):
	comments = await db["comments"].find({"postId": ObjectId(post_id)}).to_list(100)
	return comments