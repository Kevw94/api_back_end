from fastapi import Request
from app.core.config import db
from app.models.auth import AuthModel


async def try_create_user(request: Request, user_auth: AuthModel):
	new_user = {
		"username": user_auth.username,
		"password": user_auth.password
	}
	db["users"].insert_one(new_user)
	return { "success": new_user }
