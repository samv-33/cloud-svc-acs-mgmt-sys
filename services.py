import asyncio
from datetime import datetime

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Path, Query
from pymongo.errors import DuplicateKeyError

from models import (
    perm_collection,
    sub_plan_collection,
    subscriptions_collection,
    usage_collection,
    users_collection,
)
from schemas import Permission, Subscription, SubscriptionPlan, Usage, User

app = FastAPI(title="Cloud Service Access Management System")


# Routes: Subscription Plan Management
@app.post("/plans")
async def create_plan(plan: SubscriptionPlan):
    result = await sub_plan_collection.insert_one(plan.model_dump())
    return {"message": "Plan created", "plan_id": str(result.inserted_id)}


@app.put("/plans/{plan_id}")
async def update_plan(plan_id: str, updates: dict):
    result = await sub_plan_collection.update_one(
        {"_id": ObjectId(plan_id)}, {"$set": updates}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No updates made")
    return {"message": "Plan updated"}


@app.delete("/plans/{plan_id}")
async def delete_plan(plan_id: str):
    result = await sub_plan_collection.delete_one({"_id": ObjectId(plan_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted"}


# Routes: Permissions
@app.post("/permissions")
async def add_permissions(permission: Permission):
    result = await perm_collection.insert_one(permission.model_dump())
    return {"message": "Permission created", "permission_id": str(result.inserted_id)}


@app.put("/permissions/{permission_id}")
async def update_permissions(permission_id: str, updates: dict):
    result = await perm_collection.update_one(
        {"_id": ObjectId(permission_id)}, {"$set": updates}
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="No updates made or permission not found"
        )
    return {"message": "Permission updated"}


@app.delete("/permissions/{permission_id}")
async def delete_permission(permission_id: str):
    result = await perm_collection.delete_one({"_id": ObjectId(permission_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted"}


@app.get("/")
async def root_page():
    return {"message": "Cloud Service Management System"}


# User Subscription Handling Route


@app.post("/users")
async def create_user(user: User):
    """Creates a new user."""
    result = await users_collection.insert_one(user.model_dump())
    return str(result.inserted_id)


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Retrieves a user by ID."""
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        raise HTTPException(status_code=404, detail="User not found")


# Implement other service functions similarly
# (e.g., create_user, get_user, create_subscription,
# get_subscription, check_access, track_usage, etc.)


@app.post("/usage/{user_id}")
async def track_usage(user_id: str, api_endpoint: str):
    """Track API usage for a user"""
    current_timestamp = datetime.utcnow().date()
    usage_record = await usage_collection.find_one(
        {"user_id": user_id, "api_endpoint": api_endpoint}
    )
    # api request has been made before
    if usage_record:
        subscription = await subscriptions_collection.find_one({"user_id": user_id})
        if usage_record["count"] >= subscription["limits"].get(api_endpoint, 0):
            raise HTTPException(
                status_code=429, detail="Usage limit exceeded for this API"
            )

        # can update usage count
        await usage_collection.update_one(
            {"_id": usage_record["id"]}, {"$inc": {"count": 1}}
        )
    else:
        # first api request: create a new usage record
        new_usage = Usage(
            user_id=user_id, api_endpoint=api_endpoint, timestamp=str(current_timestamp)
        )
        await usage_collection.insert_one(new_usage.dict())
    return {"message": "API usage has been tacked!!"}

