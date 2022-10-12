from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import config
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.auth import TokenData
from app.models.users import UserModel
from app.core.config import db
# from pydantic import BaseModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(UserModel):
    hashed_password: str

def get_password_hash(password: str):
	"""hash a password

	Args:
		password (str): password get for creating a user 

	Returns:
		str: hashed password
	"""
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
	"""check if password and hashed password from db matches together

	Args:
		plain_password (str): password from login 
		hashed_password (str): password from db

	Returns:
		Bool: if matches return True or False
	"""
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	"""Take username and create an access token for this user who wants to login

	Args:
		data (dict): get the username
		expires_delta (timedelta | None, optional): expiration for the token created. Defaults to None.

	Returns:
		str: jwt token created for the user logged
	"""
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
	return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, config["SECRET_KEY"], algorithms=config["ALGORITHM"])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except JWTError:
		raise credentials_exception
	user = await db["users"].find_one({
		"username": username
	})
	print(user, "user")
	if user is None:
		raise credentials_exception
	return user



async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
	is_disabled_user = current_user["disabled"]
	if is_disabled_user:
		raise HTTPException(status_code=400, detail="Inactive user")
	return current_user