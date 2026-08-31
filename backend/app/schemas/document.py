from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    category: str = Field(default="General")
    department: Optional[str] = None
    academic_year: Optional[str] = None
    description: Optional[str] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    academic_year: Optional[str] = None
    description: Optional[str] = None

class DocumentResponse(BaseModel):
    id: str
    title: str
    filename: str
    category: str
    department: Optional[str] = None
    academic_year: Optional[str] = None
    description: Optional[str] = None
    processing_status: str
    processing_error: Optional[str] = None
    uploaded_by: str
    created_at: datetime
    updated_at: datetime
    chunk_count: Optional[int] = 0

    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int

class DocumentStatsResponse(BaseModel):
    total_documents: int
    ready_documents: int
    processing_documents: int
    failed_documents: int
    total_chunks: int
    total_users: int
    total_questions: int
