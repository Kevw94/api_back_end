from app.core.config import db
from app.models.users import ModifPasswordModel, UserModel
from bson import ObjectId
from datetime import datetime, timedelta
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.config import config

async def get_all_users():
	"""Get all users in database

	Returns:
		list of UserToFrontModel: return list of all user found in DB
	"""
	return await db["users"].find().to_list(100)


async def try_change_username(current_user: UserModel, modif_username: UserModel):
	"""Try to change the username of the current_user

	Args:
		current_user (UserModel): current_user
		modif_username (UserModel): JSON format with the current password of the user and the modified he wants to

	Returns:
		success: access new token for the user with the other password
	"""
	is_username_exists = await db["users"].find_one({'username': modif_username.username})

	if is_username_exists == None:
		await db["users"].update_one({"_id": ObjectId(current_user["_id"])}, {"$set": {"username": modif_username.username}})
		is_user_created = await db["users"].find_one({"username": modif_username.username})

		access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
		access_token = create_access_token(data={"sub": is_user_created["username"]}, expires_delta=access_token_expires)

		return {"access_token": access_token, "token_type": "bearer"}
	else:
		return {"error": "userName already exists"}
	


async def try_find_user(user_profile_to_follow: UserModel):
	"""Try to find a user with its ID To retreive the user current_user wants to follow

	Args:
		user_profile_to_follow (UserModel): User to follow

	Raises:
		Exception: Exeption

	Returns:
		UserModel: User current_user wants to follow
	"""
	find_to_follow = await db["users"].find_one({'_id': ObjectId(user_profile_to_follow)})
	if find_to_follow == None:
		raise Exception
	else:
		return find_to_follow


async def try_check_current_password(current_user: UserModel, modif_password: ModifPasswordModel):
	"""Check if the current password of the user is correct

	Args:
		current_user (UserModel): curent_user
		modif_password (ModifPasswordModel): JSON with the current_password of the current_user 

	Returns:
		UserModel: If all check passed the current_user is returned
	"""
	is_user_found = await db["users"].find_one({
		"_id": ObjectId(current_user["_id"])
	})
	if is_user_found != None:
		hashed_password = verify_password(modif_password.current_password, is_user_found["password"])
		if hashed_password:
			return is_user_found
		else:
			return False
	else:
		return False


async def try_change_password(is_user_checked: UserModel, modif_password: ModifPasswordModel):
	"""Get the hashed new password and update the okder password of the user

	Args:
		is_user_checked (UserModel): curent_user
		modif_password (ModifPasswordModel): JSON with the modified password of the current_user in

	Returns:
		Bool: True if password has been inserted
	"""
	new_password_hash = get_password_hash(modif_password.modified_password)
	await db["users"].update_one({"_id": ObjectId(is_user_checked["_id"])}, {"$set": {"password": new_password_hash}})
	return True