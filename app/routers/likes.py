from typing import List

from app.core.config import config
from fastapi import APIRouter, Body, Depends

from app.core.security import get_current_active_user
from app.crud.crud_likes import crud_post_like, crud_get_me_likes, crud_get_post_likes, crud_delete_like
from app.models.likes import LikeModel
from app.models.posts import PostModel
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post('/likes/{post_id}', response_description="Post liked",
             dependencies=[Depends(get_current_active_user)])
async def post_like(post_id: str, like: LikeModel = Body(...)):
    """Creates a like in db

    Args:
        post_id: targeted post's Id
        like: Model to send

    Returns:success message

    """
    return await crud_post_like(post_id, like)


@router.get("/likes/posts/me", response_description="List of your like posts", response_model=List[PostModel])
async def get_me_likes(current_user: UserModel = Depends(get_current_active_user)):
    """Gets all your liked posts

    Args:
        current_user: current user's Id

    Returns:
        object: list of all your posts

    """
    return await crud_get_me_likes(current_user)


@router.get("/likes/posts/{post_id}", response_description="List of post's likes", response_model=List[UserModel],
            dependencies=[Depends(get_current_active_user)])
async def get_post_likes(post_id: str):
    """Gets list of users who liked a post

    Args:
        post_id: targeted post's Id

    Returns:
        object: list of users

    """
    return await crud_get_post_likes(post_id)


@router.delete("/likes/{post_id}", response_description="Your like was successfully removed",
               dependencies=[Depends(get_current_active_user)])
async def delete_like(post_id: str):
    """Deletes a like

    Args:
        post_id: post's targeted Id to remove linked like

    Returns:
        object: success message

    """
    return await crud_delete_like(post_id)
