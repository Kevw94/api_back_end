from app.core.config import config
from datetime import datetime, timedelta
from app.core.config import db
from app.models.auth import AuthModel, LoginModel
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def try_create_user(user_auth: AuthModel):
	hashed_password = get_password_hash(user_auth.password)
	print(hashed_password)
	created_at = datetime.now()
	new_user = {
		"username": user_auth.username,
		"password": hashed_password,
		"created_at": created_at
	}
	db["users"].insert_one(new_user)
	return { "success": new_user }


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def user_logged(user_login: LoginModel):
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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return encoded_jwt