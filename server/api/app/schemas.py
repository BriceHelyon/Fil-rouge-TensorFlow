from typing import Optional
from datetime import datetime, date


from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    status: int
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    access_token_type: Optional[str] = None
    error_message: Optional[str] = None
    
    
class Response(BaseModel):
    status: int
    error_message: Optional[str] = None
    
    
class tokenData(BaseModel):
    token: str
    
class login(BaseModel): 
    email: EmailStr
    # email: str
    password: str
    
class Status(BaseModel):
    message: str

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    role: int  # 0 pour un rôle standard, 1 pour un rôle admin
    password: str

class EquipementCreate(BaseModel): 
    name: str
    starting_date: str 
    ending_date: str
    room_id: str 

class InterventionCreate(BaseModel):
    name: str
    description: str
    starting_date: datetime
    ending_date: datetime
    execution: int  
    user_id: int
    equipement_id: int

# UserOutSchema = pydantic_model_creator(
#     User, name="UserOut", exclude=["password", "created_at", "modified_at"]
# )