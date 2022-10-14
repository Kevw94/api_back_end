from pymongo import MongoClient
from fastapi import FastAPI
from app.core.config import config
from app.routers import auth, comments, followers, users, root, posts, likes


app = FastAPI(
    docs_url=f"{config['APP_PREFIX']}/docs",
    redoc_url=f"{config['APP_PREFIX']}/redoc",
)

app.include_router(users.router, tags=["users"])
app.include_router(root.router, tags=["root"])
app.include_router(auth.router, tags=["auth"])
app.include_router(posts.router, tags=["posts"])
app.include_router(followers.router, tags=["followers"])
app.include_router(comments.router, tags=["comments"])
app.include_router(likes.router, tags=["likes"])

