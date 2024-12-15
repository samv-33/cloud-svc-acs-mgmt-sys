from models import *
from schemas import *
from bson import ObjectId

def create_user(user_data: User):
    """Creates a new user."""
    result = users_collection.insert_one(user_data.model_dump())
    return str(result.inserted_id)

def get_user(user_id):
    """Retrieves a user by ID."""
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return user
    else:
        return None

# Implement other service functions similarly 
# (e.g., create_user, get_user, create_subscription, 
# get_subscription, check_access, track_usage, etc.)