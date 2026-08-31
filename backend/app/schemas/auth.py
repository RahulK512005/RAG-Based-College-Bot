from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserSignup(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
