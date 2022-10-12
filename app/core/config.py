from dotenv import dotenv_values
import motor.motor_asyncio

config = dotenv_values('./.env')

client = motor.motor_asyncio.AsyncIOMotorClient(config["MONGO_URI"])
db = client.twitter