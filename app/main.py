from pymongo import MongoClient
from fastapi import FastAPI
from app.core.config import config
from app.routers import auth, comments, followers, users, root, posts, likes, messages

app = FastAPI(
    docs_url=f"{config['APP_PREFIX']}/docs",
    redoc_url=f"{config['APP_PREFIX']}/redoc",
)

app.include_router(users.router, tags=["Users"])
app.include_router(root.router, tags=["Root"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(posts.router, tags=["Posts"])
app.include_router(followers.router, tags=["Followers"])
app.include_router(comments.router, tags=["Comments"])
app.include_router(likes.router, tags=["Likes"])
app.include_router(messages.router, tags=["Messages"])
