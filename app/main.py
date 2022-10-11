from pymongo import MongoClient
from fastapi import FastAPI
from app.core.config import config
from app.routers import users, root

app = FastAPI(
    docs_url=f"{config['APP_PREFIX']}/docs",
    redoc_url=f"{config['APP_PREFIX']}/redoc",
)

app.include_router(users.router)
app.include_router(root.router)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGO_URI"])
    app.mongodb = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

