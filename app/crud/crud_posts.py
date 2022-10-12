import datetime

from bson import ObjectId

from app.core.config import db
from app.models.posts import PostModel, PatchModel


async def crud_get_all_posts():
    return await db["posts"].find().to_list(500)


async def crud_create_post(post: PostModel):
    created_at = datetime.datetime.now()
    new_post = {
        "userId": post.userId,
        "content": post.content,
        "created_at": created_at
    }
    db['posts'].insert_one(new_post)
    return {"success": "Post created"}


async def crud_patch_post(post_id, patch):
    db['posts'].update_one({"_id": ObjectId(post_id)},
                           {"$set": {"content": patch.content}}
                           )
    return {"Successful": 'Updated post'}
