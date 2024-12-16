#from fastapi import FastAPI, Path, Query, HTTPException
#from pymongo.errors import DuplicateKeyError
#from motor.motor_asyncio import AsyncIOMotorClient
#from pydantic import BaseModel, Field
#from typing import List, Dict
#import asyncio
#from bson.objectid import ObjectId
#
#app=FastAPI(title="Cloud Service Access Management System")
#
#
##Database configurations
#mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
#db = mongo_client["my_database"]
#
##collections
#sub_plan_collection = db["sub_plan_collection"]
#perm_collection = db["perm_collection"]
#
#class SubscriptionPlan(BaseModel):
#    name: str
#    description: str
#    api_permissions: List[str]
#    usage_limits: Dict[str, int]
#
#class Permission(BaseModel):
#    name: str
#    description: str
#    api_endpoint: str
#
#
##Routes: Subscription Plan Management
#@app.post("/plans")
#async def create_plan(plan: SubscriptionPlan):
#    result = await sub_plan_collection.insert_one(plan.model_dump()) 
#    return {"message": "Plan created", "plan_id": str(result.inserted_id)}
#
#
#@app.put("/plans/{plan_id}")
#async def update_plan(plan_id: str, updates: dict):
#    result = await sub_plan_collection.update_one({"_id": ObjectId(plan_id)}, {"$set": updates})
#    if result.modified_count == 0:
#        raise HTTPException(status_code=404, detail="No updates made")
#    return {"message": "Plan updated"}
#
#@app.delete("/plans/{plan_id}")
#async def delete_plan(plan_id: str):
#    result = await sub_plan_collection.delete_one({"_id": ObjectId(plan_id)})
#    if result.deleted_count == 0:
#        raise HTTPException(status_code=404, detail="Plan not found")
#    return {"message": "Plan deleted"}
#
## Routes: Permissions
#@app.post("/permissions")
#async def add_permissions(permission: Permission):
#    result = await perm_collection.insert_one(permission.model_dump())
#    return {"message": "Permission created", "permission_id": str(result.inserted_id) }
#
#@app.put("/permissions/{permission_id}")
#async def update_permissions(permission_id: str, updates: dict):
#    result = await perm_collection.update_one({"_id": ObjectId(permission_id)}, {"$set": updates})
#    if result.modified_count == 0:
#        raise HTTPException(status_code=404, detail="No updates made or permission not found")
#    return {"message": "Permission updated"}
#
#@app.delete("/permissions/{permission_id}")
#async def delete_permission(permission_id: str):
#    result = await perm_collection.delete_one({"_id": ObjectId(permission_id)})
#    if result.deleted_count == 0:
#        raise HTTPException(status_code=404, detail="Permission not found")
#    return {"message": "Permission deleted"}
#
#@app.get("/")
#async def root_page():
#    return {"message": "Cloud Service Management System"}



