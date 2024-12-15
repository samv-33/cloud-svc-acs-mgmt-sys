from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str 

class Plan(BaseModel):
    name: str
    description: str
    permissions: list[str] 
    limits: dict 

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