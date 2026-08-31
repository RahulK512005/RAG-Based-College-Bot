from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class FeedbackCreate(BaseModel):
    rating: int = Field(..., description="1 for positive, -1 for negative")
    comment: Optional[str] = Field(None, max_length=1000)

class FeedbackResponse(BaseModel):
    id: str
    message_id: str
    user_id: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
