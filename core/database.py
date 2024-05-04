import motor.motor_asyncio
import os
from dotenv import load_dotenv
load_dotenv()
MONGO_DETAILS = os.getenv("MONGO")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.pharma

pharmacy = database.get_collection("pharmacies")
users = database.get_collection("users")
