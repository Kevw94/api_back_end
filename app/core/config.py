from dotenv import dotenv_values
import motor.motor_asyncio

config = dotenv_values('./.env')

# init connection for the and the name of the db to connect to it
client = motor.motor_asyncio.AsyncIOMotorClient(config["MONGO_URI"])
db = client.twitter