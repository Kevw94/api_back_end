from fastapi import APIRouter

from app.core.config import config

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/", response_description="For testing first connection of the API", responses={200: {"description": "Welcome message"}})
def root():
    return {"message": "Welcome to TWITWI API"}
