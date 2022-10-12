from app.core.config import config
from fastapi import APIRouter
from typing import List
from app.crud.crud_messages import get_all_messages
from app.models.messages import MessageModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)

@router.get("/messages", response_description="List all messages", response_model=List[MessageModel])
async def get_messages():
    return await get_all_messages()
