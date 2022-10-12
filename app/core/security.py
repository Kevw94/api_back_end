from passlib.context import CryptContext
from jose import jwt
from app.core.config import config
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

