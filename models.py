from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch configurations from environment variables
mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DATABASE_NAME")

#Database configurations
mongo_client = AsyncIOMotorClient(mongo_uri)
db = mongo_client["my_database"]

# Define collections 
users_collection = db["users_collection"]
sub_plan_collection = db["sub_plan_collection"]
perm_collection = db["perm_collection"]
subscriptions_collection = db["subscriptions_collection"]
usage_collection = db["usage_collection"] 

