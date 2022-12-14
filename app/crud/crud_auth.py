from datetime import datetime
from app.core.config import db
from app.core.security import get_password_hash, verify_password
from app.models.auth import AuthModel, LoginModel
from fastapi import HTTPException, status


async def try_create_user(user_auth: AuthModel):
	"""Insert and create one user in DB, create an hashed password

	Args:
		user_auth (AuthModel): accept a username and pssword from the Body

	Raises:
		credentials_exception: user already exists in DB -> prevent duplicate

	Returns:
		success: 201
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_403_FORBIDDEN,
		detail="This username is already in use",
	)
	is_username_exists = await db["users"].find_one({"username": user_auth.username})
	if is_username_exists != None:
		raise credentials_exception
	else:
		hashed_password = get_password_hash(user_auth.password)
		created_at = datetime.now()
		new_user = {
			"username": user_auth.username,
			"password": hashed_password,
			"created_at": created_at,
			"disabled": False
		}
		db["users"].insert_one(new_user)
		return "success"



async def try_login_user(user_login: LoginModel):
	"""Verify if user exists in DB, if yes, verify if password matches

	Auth a user: verify if the user exists ans if the hash of the password mathes with verify_password

	Args:
		user_login (LoginModel): Body from request containing password and username

	Returns:
		UserModel: user if user pass check tests
	"""
	is_user_found = await db["users"].find_one({
		"username": user_login.username
	})
	if is_user_found != None:
		hashed_password = verify_password(user_login.password, is_user_found["password"])
		if hashed_password:
			return is_user_found
		else:
			return False
	else:
		return False
