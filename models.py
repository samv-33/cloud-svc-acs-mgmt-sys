from motor.motor_asyncio import AsyncIOMotorClient

#client = MongoClient(MONGO_URI)
#db = client["cloud_access"]

#Database configurations
mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["my_database"]

# Define collections 
users_collection = db["users_collection"]
sub_plan_collection = db["sub_plan_collection"]
perm_collection = db["perm_collection"]
subscriptions_collection = db["subscriptions_collection"]
usage_collection = db["usage_collection"] 

