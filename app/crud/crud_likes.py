import datetime

from bson import ObjectId

from app.core.config import db
from app.models.likes import LikeModel
from app.models.users import UserModel
from fastapi import HTTPException, status



async def crud_post_like(post_id, like: UserModel):
	credentials_exception = HTTPException(
		status_code=status.HTTP_403_FORBIDDEN,
		detail="This like already exits",
	)
	credentials_exception_problem = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with creating like try again",
	)
	is_like_exists = await db["likes"].find_one({"$and": [{"userId": like["_id"], "postId": ObjectId(post_id)}]})
	if is_like_exists is None:
		created_at = datetime.datetime.now()
		new_like = {
			"userId": like["_id"],
			"postId": ObjectId(post_id),
			"created_at": created_at
		}
		db['likes'].insert_one(new_like)
		is_like_inserted = await db["likes"].find_one({"$and": [{"userId": like["_id"], "postId": ObjectId(post_id), "created_at": created_at}]})
		if is_like_inserted is not None:
			return {"success": "Like added"}
		else:
			raise credentials_exception_problem
	else:
		raise credentials_exception


async def crud_get_me_likes(user_data):
    """Gets all posts current user

    Args:
        user_data: current user's info containing his Id

    Returns:
        object: list of my liked posts

    """
    posts = []
    liked_posts = await db['likes'].find({'userId': user_data['_id']}).to_list(1000)
    for like in liked_posts:
        posts.append(await db['posts'].find_one({'_id': ObjectId(like['postId'])}))
    return posts


async def crud_get_post_likes(post_id):
    """Gets list of users who liked a post

    Args:
        post_id: targeted post's Id

    Returns:
        object: list of users

    """
    users = []
    posts = await db['likes'].find({'postId': ObjectId(post_id)}).to_list(1000)
    for like in posts:
        users.append(await db['users'].find_one({"_id": ObjectId(like['userId'])}))
    return users



async def crud_delete_like(like_id):
    """Deletes a like on a post

    Args:
        like_id: targeted like Id

    Returns:
        object: success message

    """
async def crud_delete_like(like_id, current_user: UserModel):
	credentials_exception_problem = HTTPException(
		status_code=status.HTTP_409_CONFLICT,
		detail="There were a problem with creating like try again",
	)
	await db["likes"].delete_one({
		"$and": 
				[
					{
						'_id': ObjectId(like_id),
						"userId": current_user["_id"]
						
					}
				]
	})

	is_like_deleted = await db["likes"].find_one({"$and": [{'_id': ObjectId(like_id), "userId": current_user["_id"]}]})
	if is_like_deleted is None:
		return {"successful": "like has been deleted"}
	else:
		raise credentials_exception_problem
