import datetime

from bson import ObjectId

from app.core.config import db
from app.models.likes import LikeModel
from app.models.users import UserModel


async def crud_post_like(post_id, like: UserModel):
	#TODO if liked return and prevent it
    created_at = datetime.datetime.now()
    new_like = {
        "userId": like["_id"],
        "postId": ObjectId(post_id),
        "created_at": created_at
    }
    db['likes'].insert_one(new_like)
    return {"success": "Like added"}


async def crud_get_me_likes(user_data):
    posts = []
    liked_posts = await db['likes'].find({'userId': user_data['_id']}).to_list(1000)
    for like in liked_posts:
        posts.append(await db['posts'].find_one({'_id': ObjectId(like['postId'])}))
    return posts


async def crud_get_post_likes(post_id):
    users = []
    posts = await db['likes'].find({'postId': ObjectId(post_id)}).to_list(1000)
    for like in posts:
        users.append(await db['users'].find_one({"_id": ObjectId(like['userId'])}))
    return users


async def crud_delete_like(like_id, current_user: UserModel):
	await db["likes"].delete_one({
		"$and": 
				[
					{
						'_id': ObjectId(like_id),
						"userId": current_user["_id"]
						
					}
				]
	})
	return {"successful": "success"}
