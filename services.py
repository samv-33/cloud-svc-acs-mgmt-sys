import asyncio
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Path, Query
from pymongo.errors import DuplicateKeyError
from typing import Dict

from models import (
    perm_collection,
    sub_plan_collection,
    subscriptions_collection,
    usage_collection,
    users_collection,
)
from schemas import Permission, Subscription, SubscriptionPlan, Usage, User
from datetime import datetime, timezone, timedelta

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
    return {"message": "New user created!", "user_id": str(result.inserted_id)}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Retrieves a user by ID."""
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return user #Return the user data
    else: #If the user is not found
        raise HTTPException(status_code=404, detail="User not found")
    


#Subscription handling

@app.post("/subscriptions")
async def create_subscriptions(subscription: Subscription):

    #Check if user exist
    user = await users_collection.find_one({"_id": ObjectId(subscription.user_id)})
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    plan = await sub_plan_collection.find_one({"_id": ObjectId(subscription.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    subscription_data = {
        "user_id": subscription.user_id,
        "plan_id": subscription.plan_id,
        "start_date": subscription.start_date.isoformat(), #Convert datetime to ISO string
        "end_date": subscription.end_date.isoformat() if subscription.end_date else None #Handle optional end_date
    }

    try:
        result = await subscriptions_collection.insert_one(subscription_data)
        return {"message": "Subscription created", "subscription_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/subscriptions/{user_id}")
async def get_subscriptions(user_id: str): 
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription["_id"] = str(subscription["_id"])
    return subscription




@app.post("/usage")
async def collect_usage_data(usage: Usage):
    """Track API usage for a user."""
    #Ensure user exists
    try:
        user_object_id = ObjectId(usage.user_id) #Convert user_id to ObjectId
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    user = await users_collection.find_one({"_id": user_object_id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #Create the usage record
    usage_data = {
        "user_id": usage.user_id,
        "api_endpoint": usage.api_endpoint,
        "timestamp": usage.timestamp or datetime.now(timezone.utc).isoformat(), #Use provided time or current time
        "api_calls": usage.api_calls, #Increment the call count for each usage entry
        "storage_used": usage.storage_used, # Add storage usage if needed
    }
    # Insert into the usage collection
    result = await usage_collection.insert_one(usage_data)
    return {"message": "Usage tracked", "usage_id": str(result.inserted_id)}




@app.get("/subscriptions/{user_id}/usage")
async def get_usage_stats(user_id: str):
    
    # Find the user's subscription
    subscription = await subscriptions_collection.find_one({"user_id": user_id})

    if not subscription:
        raise HTTPException(status_code=404, detail="User subscription not found")
    
    #Retrieve usage statistics for the user
    usage_data = await usage_collection.find({"user_id": user_id}).to_list(100)

    if not usage_data:
        raise HTTPException(status_code=404, detail="No usage data found for this user")
    
    #Calculate the usage statistics
    total_api_calls = sum(usage.get("api_calls", 0) for usage in usage_data)
    total_storage_used = sum(usage.get("storage_used", 0) for usage in usage_data)

        # Handle plan_id format (ObjectId or string)
    plan_id = subscription["plan_id"]

    try:
        # If plan_id is a string, try converting to ObjectId
        plan_id = ObjectId(plan_id)
    except Exception:
        # If plan_id can't be converted, assume it's a string and query as-is
        pass

    # Query the subscription plan
    subscription_plan = await sub_plan_collection.find_one({"_id": plan_id})

    # Initialize response fields
    remaining_daily = None
    remaining_monthly = None

    if subscription_plan and "usage_limits" in subscription_plan:
        usage_limits = subscription_plan["usage_limits"]

        # Check for 'daily' limit
        if "daily" in usage_limits:
            daily_limit = usage_limits["daily"]
            remaining_daily = max(daily_limit - total_api_calls, 0)

        # Check for 'monthly' limit
        if "monthly" in usage_limits:
            monthly_limit = usage_limits["monthly"]
            remaining_monthly = max(monthly_limit - total_api_calls, 0)

        usage_stats = {
            "total_api_calls": total_api_calls,
            "total_storage_used": total_storage_used,
            "remaining_daily": remaining_daily,
            "remaining_monthly": remaining_monthly
        }

        return usage_stats
    



@app.put("/subscriptions/{user_id}")
async def assign_modify_user_plan(user_id: str, plan_id: str):
    # Validate the plan ID
    plan = await sub_plan_collection.find_one({"_id": ObjectId(plan_id)})

    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    
    #Check if the user has an existing subscription
    exist_subscription = await subscriptions_collection.find_one({"user_id": user_id})

    if not exist_subscription:
        raise HTTPException(status_code=400, detail="User does not have an existing subscription")

    # Prepare subscription details
    updated_subscription = {
        "user_id": user_id,
        "plan_id": plan_id,
        "start_date": datetime.now(timezone.utc).isoformat(),
        "end_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),  # Default 30-day duration
        "status": "active"
    }

    # Modify the existing subscription
    result = await subscriptions_collection.update_one(
        {"user_id": user_id},  # Filter by user_id
        {"$set": updated_subscription}  # Update the subscription data
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update subscription")

    return {"message": "User subscription updated successfully", "subscription": updated_subscription}





@app.get("/access/{user_id}/{api_endpoint}")
async def check_access(user_id: str, api_endpoint: str):
    # Retrieve the user's subscription from the database
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Retrieve the plan details associated with the subscription
    plan = await sub_plan_collection.find_one({"_id": ObjectId(subscription["plan_id"])})
    if not plan:
        raise HTTPException(status_code=403, detail="Access denied for this API endpoint")

    # Check if the requested API endpoint is allowed under the current plan
    if api_endpoint not in plan["api_permissions"]:
        raise HTTPException(status_code=403, detail="This API endpoint is not allowed under your subscription plan")

    # Retrieve usage data for the user (e.g., API calls, storage used)
    usage_data = await usage_collection.find({"user_id": user_id}).to_list(100)
    if not usage_data:
        raise HTTPException(status_code=404, detail="No usage data found for this user")
    
    # Calculate the total API calls made by the user
    total_api_calls = sum(usage.get("api_calls", 0) for usage in usage_data)
    
    # Check usage limits (e.g., daily or monthly limits) based on the subscription plan
    daily_limit = plan.get("usage_limits", {}).get("daily", 0)
    monthly_limit = plan.get("usage_limits", {}).get("monthly", 0)

    # If limits exist, check if the user has exceeded them
    if daily_limit > 0 and total_api_calls >= daily_limit:
        raise HTTPException(status_code=403, detail="API daily limit exceeded")
    if monthly_limit > 0 and total_api_calls >= monthly_limit:
        raise HTTPException(status_code=403, detail="API monthly limit exceeded")
    
    # If all checks pass, allow access
    return {"access": True, "message": "API access granted"}


#@app.post("/usage/{user_id}")
#async def track_usage(user_id: str, api_endpoint: str, usage_limits: Dict[str, int]):
#    """Track API usage for a user"""
#    current_timestamp = datetime.now(timezone.utc).date()
#    usage_record = await usage_collection.find_one(
#        {"user_id": user_id, "api_endpoint": api_endpoint}
#    )
#    # api request has been made before
#    if usage_record:
#        subscription = await subscriptions_collection.find_one({"user_id": user_id})
#        usage_limit = await sub_plan_collection.find_one({"usage_limits": usage_limits})
#        subscription["limits"] = usage_limit
#
#        # Ensure " count " exists before comparing it to the subscription limit
#        if "count" not in usage_record:
#            usage_record["count"] = 0 # Initialize count if not present
#
#
#        if usage_record["count"] >= subscription["limits"].get(api_endpoint, 0):
#            raise HTTPException(
#                status_code=429, detail="Usage limit exceeded for this API"
#            )
#
#        # can update usage count
#        await usage_collection.update_one(
#            {"_id": usage_record["_id"]}, {"$inc": {"count": 1}}
#        )
#    else:
#        # first api request: create a new usage record
#        new_usage = Usage(
#            user_id=user_id,
#            api_endpoint=api_endpoint, 
#            timestamp=str(current_timestamp),
#        )
#        await usage_collection.insert_one(new_usage.model_dump())
#
#    return {"message": "API usage has been tracked!!"}

@app.post("/usage/{user_id}")
async def track_usage(user_id: str, api_endpoint: str):

     """Track API usage for a user"""
     current_timestamp = datetime.now(timezone.utc).date()

     usage_record = await usage_collection.find_one(
        {"user_id": user_id, "api_endpoint": api_endpoint}
    )
    
    # API request has been made before
     if usage_record:
        subscription = await subscriptions_collection.find_one({"user_id": user_id})
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
         # Get the usage limits from the subscription plan
        plan = await sub_plan_collection.find_one({"_id": ObjectId(subscription["plan_id"])})
        if not plan or "usage_limits" not in plan:
            raise HTTPException(status_code=404, detail="No usage limits found for this plan")
        
        usage_limits = plan["usage_limits"]
        if api_endpoint not in usage_limits:
            raise HTTPException(status_code=403, detail="This API endpoint is not allowed under your subscription plan")


        # Ensure "count" exists before comparing it to the subscription limit
        if "count" not in usage_record:
            usage_record["count"] = 0  # Initialize count if not present

        ## Check if usage exceeds the limit
        #if usage_record["count"] >= subscription["limits"].get(api_endpoint, 0):
        #    raise HTTPException(
        #        status_code=429, detail="Usage limit exceeded for this API"
        #    )
        # Check if usage exceeds the limit
        if usage_limits[api_endpoint]["daily"] > 0 and usage_record["count"] >= usage_limits[api_endpoint]["daily"]:
            raise HTTPException(status_code=429, detail="API daily limit exceeded")

        # Update usage count
        await usage_collection.update_one(
            {"_id": usage_record["_id"]}, {"$inc": {"count": 1}}
        )
     else:
        # First API request: create a new usage record
        new_usage = Usage(
            user_id=user_id,
            api_endpoint=api_endpoint,
            timestamp=str(current_timestamp),
        )
        await usage_collection.insert_one(new_usage.model_dump())

     return {"message": "API usage has been tracked!"}




#@app.get("/usage/{user_id}/limit")
#async def check_usage_limit(user_id: str, api_endpoint: str):
#    """Check the usage limit status for a user"""
#    usage_record = await usage_collection.find_one(
#        {"user_id": user_id, "api_endpoint": api_endpoint}
#    )
#    
#    if not usage_record:
#        raise HTTPException(
#            status_code=404, detail="No usage record found for this API endpoint"
#        )
#    
#    subscription = await subscriptions_collection.find_one({"user_id": user_id})
#    if not subscription:
#        raise HTTPException(
#            status_code=404, detail="No subscription found for this user"
#        )
#
#    usage_limit = await sub_plan_collection.find_one({"plan_id": subscription.get("plan_id")})
#    if not usage_limit:
#        raise HTTPException(
#            status_code=404, detail="No usage limits found for this subscription"
#        )
#
#    limit = usage_limit.get("usage_limits", {}).get(api_endpoint, 0)
#    if limit == 0:
#        raise HTTPException(
#            status_code=404, detail="No usage limit defined for this API endpoint"
#        ) 
#    
#    # Get the current count and the limit for the given api_endpoint
#    current_count = usage_record.get("count", 0)
#
#    return {
#        "user_id": user_id,
#        "api_endpoint": api_endpoint,
#        "current_usage": current_count,
#        "limit": limit,
#        "remaining_usage": max(limit - current_count, 0),
#    }
#

@app.get("/usage/{user_id}/limit")
async def check_usage_limit(user_id: str, api_endpoint: str):
    """Check the usage limit status for a user"""
    
    # Check if the usage record exists for the user and API endpoint
    usage_record = await usage_collection.find_one({"user_id": user_id, "api_endpoint": api_endpoint})
    
    if not usage_record:
        raise HTTPException(
            status_code=404, detail="No usage record found for this API endpoint"
        )
    
    # Check if the subscription exists for the user
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(
            status_code=404, detail="No subscription found for this user"
        )

    # Fetch the usage limit based on the user's subscription plan
    usage_limit = await sub_plan_collection.find_one({"plan_id": subscription.get("plan_id")})
    if not usage_limit:
        raise HTTPException(
            status_code=404, detail="No usage limits found for this subscription"
        )
    
    # Ensure usage_limits is a dictionary and contains the api_endpoint
    usage_limits = usage_limit.get("usage_limits", {})
    if not isinstance(usage_limits, dict):
        raise HTTPException(
            status_code=500, detail="Invalid structure of usage limits in the subscription plan"
        )

    limit = usage_limits.get(api_endpoint, None)
    if limit is None:
        raise HTTPException(
            status_code=404, detail="No usage limit defined for this API endpoint"
        )

    # Get the current count for the api_endpoint usage
    current_count = usage_record.get("count", 0)

    return {
        "user_id": user_id,
        "api_endpoint": api_endpoint,
        "current_usage": current_count,
        "limit": limit,
        "remaining_usage": max(limit - current_count, 0),
    }


