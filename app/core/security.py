from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import config
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from app.models.auth import TokenData
from app.models.users import UserModel
from app.core.config import db


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


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
	"""Decode JWT token sent in headers and try to find user in db with information

	Args:
		token (str): JWT present in headers. Defaults to Depends(oauth2_scheme).

	Raises:
		credentials_exception: no Authorization found
		credentials_exception: if user is not present in the decode
		credentials_exception: if user is not found in the db 

	Returns:
		UserModel: return user 
	"""
	if security_scopes.scopes:
		authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
	else:
		authenticate_value = f"Bearer"
		credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": authenticate_value},
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
	if user is None:
		raise credentials_exception
	return user



async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
	"""get active user with headers in request

	Args:
		current_user (UserModel): user retreived from db. Defaults to Depends(get_current_user).

	Raises:
		HTTPException: if user is disabled

	Returns:
		UserModel: return user found in db
	"""
	is_disabled_user = current_user["disabled"]
	if is_disabled_user:
		raise HTTPException(status_code=400, detail="Inactive user")
	return current_user