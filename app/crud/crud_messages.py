import datetime

from bson import ObjectId
from fastapi import HTTPException, status

from app.core.config import db
from app.models.messages import MessageModel

credentials_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No messages",
)
credentials_exception_problem = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="There were a problem with updating user in db, try again",
)


async def crud_get_messages(contact_id, current_user):
    """Gets messages between current user and other user

    Args:
        contact_id: target other user Id
        current_user: contains current user infos

    Returns:
        object: JSON of all messages

    """
    messages = await db['messages'].find({
        "$or":
            [
                {"senderId": ObjectId(current_user['_id'])},
                {"receiverId": ObjectId(current_user['_id'])},
                {"senderId": ObjectId(contact_id)},
                {"receiverId": ObjectId(contact_id)}
            ]
    }).to_list(1000)
    if len(messages) > 0:
        return messages
    else:
        raise credentials_exception


async def crud_post_message(current_user, message: MessageModel):
    """Post message with given body to targeted other user

    Args:
        current_user: contains current user Id
        message: body to send to db

    Returns:
        success message

    """
    created_at = datetime.datetime.now()
    new_message = {
        "senderId": ObjectId(current_user["_id"]),
        "receiverId": ObjectId(message.receiverId),
        "message": message.message,
        "created_at": created_at
    }
    await db['messages'].insert_one(new_message)
    find_msg = await crud_get_messages(message.receiverId, current_user)
    print(find_msg)
    try:
        if len(find_msg) > 0:
            return {"success": "message sent"}
    except:
        raise credentials_exception_problem
