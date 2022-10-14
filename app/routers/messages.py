from typing import List

from fastapi import Body, Depends
from app.core.config import config
from fastapi import APIRouter

from app.core.security import get_current_active_user
from app.crud.crud_messages import crud_get_messages, crud_post_message
from app.models.messages import MessageModel, GetMessageModel
from app.models.users import UserModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get('/messages/{contact_id}', response_description="Your conversation messages",
            response_model=List[GetMessageModel])
async def get_messages(contact_id, current_user: UserModel = Depends(get_current_active_user)):
    """Gets messages between current user and other user

    Args:
        contact_id: targeted other user
        current_user: contains current user infos

    Returns:
        JSON of messages

    """
    return await crud_get_messages(contact_id, current_user)


@router.post("/messages", response_description="Message sent")
async def post_message(message: MessageModel = Body(...), current_user: UserModel = Depends(get_current_active_user)):
    """Post message with body data

    Args:
        message: string to send to db
        current_user: current user infos contains his Id

    Returns: success message

    """
    return await crud_post_message(current_user, message)
