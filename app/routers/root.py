from fastapi import APIRouter

from app.core.config import config

router = APIRouter(
    prefix=f"{config['APP_PREFIX']}"
)


@router.get("/")
def root():
    return {"message": "Welcome to the PyMongo tutorial!"}
