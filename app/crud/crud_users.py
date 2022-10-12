from app.core.config import db

async def get_all_users():
	return await db["users"].find().to_list(100)