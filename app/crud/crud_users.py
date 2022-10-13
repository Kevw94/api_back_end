from app.core.config import db
from app.models.users import UserModel
from bson import ObjectId
from datetime import datetime, timedelta
from app.core.security import create_access_token
from app.core.config import config

async def get_all_users():
	return await db["users"].find().to_list(100)


async def try_change_username(current_user: UserModel, modif_username: UserModel):
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
	find_to_follow = await db["users"].find_one({'_id': ObjectId(user_profile_to_follow)})
	if find_to_follow == None:
		raise Exception
	else:
		return find_to_follow