from datetime import datetime
from app.core.config import db
from bson import ObjectId


async def try_insert_followers(current_user, create_followers):
	created_at = datetime.now()
	is_user_followed_exists = await  db["users"].find_one({"followingId": create_followers.followingId })
	is_user_followed = await db["followers"].find_one({"$and": [{"followingId": create_followers.followingId, "userId": current_user["_id"]}]})
	if is_user_followed == None and is_user_followed_exists != None:
		new_follower = {
		"userId": current_user["_id"], 
		"followingId": create_followers.followingId,
		"created_at": created_at
		}
		db["followers"].insert_one(new_follower)
		return True
	else:
		# TODO Raise exception
		return False
	
