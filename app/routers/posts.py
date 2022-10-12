from bson import ObjectId
from fastapi import Body
from app.core.config import config
from fastapi import APIRouter
from typing import List
from app.crud.crud_posts import crud_get_all_posts, crud_create_post, crud_patch_post
from app.models.posts import PostModel, PatchModel

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
