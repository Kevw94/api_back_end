from pymongo import MongoClient
from fastapi import FastAPI
from app.core.config import config
from app.routers import auth, followers, users, root, posts

app = FastAPI(
    docs_url=f"{config['APP_PREFIX']}/docs",
    redoc_url=f"{config['APP_PREFIX']}/redoc",
)

app.include_router(users.router)
app.include_router(root.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(followers.router)
