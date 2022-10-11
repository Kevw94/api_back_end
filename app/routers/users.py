from app.core.config import config
from fastapi import APIRouter

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/users", response_description="Add new user")
def get_user():
    return {"message": "user"}


