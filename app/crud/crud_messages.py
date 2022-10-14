import datetime

from bson import ObjectId

from app.core.config import db
from app.models.messages import MessageModel


async def crud_get_messages(contact_id, current_user):
    """Gets messages between current user and other user

    Args:
        contact_id: target other user Id
        current_user: contains current user infos

    Returns:
        object: JSON of all messages

    """
    return await db['messages'].find({
        "$or":
            [
                {"senderId": ObjectId(current_user['_id'])},
                {"receiverId": ObjectId(current_user['_id'])},
                {"senderId": ObjectId(contact_id)},
                {"receiverId": ObjectId(contact_id)}
            ]
    }).to_list(1000)


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
    return {"success": "message sent"}
