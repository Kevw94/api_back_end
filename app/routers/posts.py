from bson import ObjectId
from fastapi import Body, Depends
from app.core.config import config
from fastapi import APIRouter
from typing import List

from app.core.security import get_current_active_user
from app.crud.crud_posts import crud_get_all_posts, crud_create_post, crud_patch_post, crud_get_me_posts, \
    crud_delete_post
from app.models.posts import PostModel, PatchModel
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/posts", response_description="List all posts", response_model=List[PostModel])
async def get_all_posts():
    return await crud_get_all_posts()


@router.post("/posts", response_description="Post created")
async def create_post(post: PostModel = Body(...)):
    return await crud_create_post(post)


@router.patch("/posts/{post_id}", response_description="Post edited")
async def patch_post(post_id: str, patch: PatchModel = Body(...)):
    return await crud_patch_post(post_id, patch)


@router.get('/posts/me', response_description="List of your posts", response_model=List[PostModel])
async def get_me_posts(current_user: UserModel = Depends(get_current_active_user)):
    return await crud_get_me_posts(current_user)


@router.delete('/posts/{post_id}', response_description="Post successfully deleted")
async def delete_post(post_id: str):
    return await crud_delete_post(post_id)