from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

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
    start_date: datetime
    end_date: Optional[datetime] = None #Optional, default None if not set

class Usage(BaseModel):
    user_id: str
    api_endpoint: str
    timestamp: Optional[datetime] = None #Optional; can be auto-populated
    api_calls: int = Field(1, description="Number of API calls made") # Default to 1
    storage_used: int = Field(0, description="Storage used in MB") # Default to 0
