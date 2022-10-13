import datetime

from bson import ObjectId

from app.core.config import db
from app.models.posts import PostModel


async def crud_get_all_posts():
    """Function to get all posts from all users

    Returns:
        object: JSON of all posts

    """
    return await db["posts"].find().to_list(500)


async def crud_create_post(post: PostModel):
    """Function to create a post and adding created_at field

    Args:
        post: accepts content field

    Returns:
        object: Success Message

    """
    created_at = datetime.datetime.now()
    new_post = {
        "userId": post.userId,
        "content": post.content,
        "created_at": created_at
    }
    db['posts'].insert_one(new_post)
    return {"success": "Post created"}


async def crud_patch_post(post_id, patch):
    """Function to edit the content of a precise post by its ID

    Args:
        post_id: ID of the targeted post
        patch: accepted Model containing the new content

    Returns:
        object: Success message

    """
    db['posts'].update_one({"_id": ObjectId(post_id)},
                           {"$set": {"content": patch.content}}
                           )
    return {"Successful": 'Updated post'}


async def crud_get_me_posts(user_data):
    """Function to get all posts by the current user

    Args:
        user_data: Current user data containing its ID

    Returns:
        object: JSON of all the current user's posts

    """
    posts = await db['posts'].find({'userId': user_data['_id']}).to_list(1000)
    return posts


async def crud_delete_post(post_id):
    """Function to delete a precise post by its ID

    Args:
        post_id: ID of the targeted post

    Returns:
        object: Success message
    """
    await db['posts'].delete_one({'_id': ObjectId(post_id)})
    return {"Successful": "Deletion successful"}
