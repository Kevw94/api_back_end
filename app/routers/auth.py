from app.core.config import config
from fastapi import APIRouter
from fastapi import Request, Body
from fastapi import HTTPException, status
from app.crud.crud_auth import create_access_token, try_create_user, user_logged
from app.core.config import db

from app.models.auth import AuthModel, LoginModel
from datetime import datetime, timedelta

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post("/signup", response_description="create user")
async def create_user(user_auth: AuthModel = Body(...)):
	await try_create_user(user_auth)


@router.post("/login", response_description="user Login")
async def try_login(user_login: LoginModel = Body(...)):
	user = await user_logged(user_login)
	print(user)
	if not user:
		raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
	access_token_expires = timedelta(minutes=30)
	access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
	return {"access_token": access_token, "token_type": "bearer"}




