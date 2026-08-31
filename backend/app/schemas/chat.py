from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class SourceSchema(BaseModel):
    document_id: str
    document_title: str
    filename: str
    page_number: Optional[int] = None
    category: str
    department: Optional[str] = None
    similarity_score: float
    excerpt: str

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    category_filter: Optional[str] = None

class FeedbackInfo(BaseModel):
    id: str
    rating: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    sources: Optional[List[SourceSchema]] = []
    created_at: datetime
    feedback: Optional[FeedbackInfo] = None

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: List[SourceSchema]
    message_id: str
    is_unknown: bool = False

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatSessionDetailResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

class CreateSessionRequest(BaseModel):
    title: Optional[str] = "New Conversation"
