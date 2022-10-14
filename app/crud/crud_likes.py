import datetime

from bson import ObjectId

from app.core.config import db
from app.models.likes import LikeModel


async def crud_post_like(post_id, like: LikeModel):
    """Creates a like in db with given post Id

    Args:
        post_id: targeted post Id 
        like: model

    Returns: success message

    """
    created_at = datetime.datetime.now()
    new_like = {
        "userId": like.userId,
        "postId": ObjectId(post_id),
        "created_at": created_at
    }
    db['likes'].insert_one(new_like)
    return {"success": "Like added"}


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
    await db['likes'].delete_one({'_id': ObjectId(like_id)})
    return {"successful": "like removed"}
