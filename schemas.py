from pydantic import BaseModel, Field
from typing import List, Dict

class User(BaseModel):
    username: str
    email: str 

class SubscriptionPlan(BaseModel):
    name: str
    description: str
    api_permissions: List[str]
    usage_limits: Dict[str, int]

class Permission(BaseModel):
    name: str
    api_endpoint: str
    description: str

class Subscription(BaseModel):
    user_id: str 
    plan_id: str
    start_date: str
    end_date: str

class Usage(BaseModel):
    user_id: str
    api_endpoint: str
    timestamp: str