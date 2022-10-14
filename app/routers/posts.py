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


@router.get("/posts", response_description="List all posts", response_model=List[PostModel], dependencies=[Depends(get_current_active_user)], responses={200: {"description": "JSON of all posts"}})
async def get_all_posts():
    """Gets all posts

    Returns: JSON of all posts

    """
    return await crud_get_all_posts()


@router.post("/posts", response_description="Post created", responses={201: {"content": {"Post created"}}, 409: {"content": {"Problem with creating post try again"}}})
async def create_post(post: PostModel = Body(...), current_user: UserModel = Depends(get_current_active_user)):
    """Creates a post with the given body

    Args:
        post: request's body containing the content

    Returns: success message

    """
    return await crud_create_post(post, current_user)


@router.patch("/posts/{post_id}", response_description="Post edited", responses={201: {"content": {"Updated post"}}, 409: {"content": {"Problem with updating posts in db"}}})
async def patch_post(post_id: str, patch: PatchModel = Body(...), current_user: UserModel = Depends(get_current_active_user)):
    """Edits the targeted post with given body

    Args:
        post_id: post's ID to edit
        patch: body containing the new data to patch existing post

    Returns: success message

    """
    return await crud_patch_post(post_id, patch, current_user)


@router.get('/posts/me', response_description="List of your posts", response_model=List[PostModel], responses={200: {"description": "JSON of all posts of the user"}})
async def get_me_posts(current_user: UserModel = Depends(get_current_active_user)):
    """Gets the current user's posts

    Args:
        current_user: userId to filter database data

    Returns: JSON of all posts

    """
    return await crud_get_me_posts(current_user)


@router.delete('/posts/{post_id}', response_description="Post successfully deleted", responses={201: {"content": {"Deletion successful"}, 409: {"content": {"Problem with updating posts in db"}}}})
async def delete_post(post_id: str, current_user: UserModel = Depends(get_current_active_user)):
    """Deletes the targeted post

    Args:
        post_id: post's id to delete

    Returns: success message

    """
    return await crud_delete_post(post_id, current_user)
