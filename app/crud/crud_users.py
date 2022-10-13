from app.core.config import db
from app.models.users import UserModel
from bson import ObjectId

async def get_all_users():
	return await db["users"].find().to_list(100)


async def try_change_username(modif_username: UserModel):
	is_username_exists = await db["users"].find_one({'username': modif_username.username})
	if is_username_exists == None:
		await db["users"].update_one({"_id": ObjectId(modif_username.id)}, {"$set": {"username": modif_username.username}})


async def try_find_user(user_profile_to_follow: UserModel):
	find_to_follow = await db["users"].find_one({'_id': ObjectId(user_profile_to_follow)})
	if find_to_follow == None:
		raise Exception
	else:
		return find_to_follow