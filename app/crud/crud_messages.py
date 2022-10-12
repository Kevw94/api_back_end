from app.core.config import db
from app.models.messages import MessageModel
async def get_all_messages():
    return await db["messages"].find().to_list(100)
