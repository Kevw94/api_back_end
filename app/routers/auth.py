from app.core.config import config
from fastapi import APIRouter
from fastapi import Request, Body
from app.crud.crud_auth import try_create_user
from app.core.config import db

from app.models.auth import AuthModel

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.post("/signup", response_description="create user")
async def create_user(request: Request, user_auth: AuthModel = Body(...)):
	await try_create_user(request, user_auth)
