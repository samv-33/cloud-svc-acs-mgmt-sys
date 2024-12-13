from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["cloud_access"]

# Define collections 
users_collection = db["users"]
plans_collection = db["plans"]
permissions_collection = db["permissions"]
subscriptions_collection = db["subscriptions"]
usage_collection = db["usage"] 