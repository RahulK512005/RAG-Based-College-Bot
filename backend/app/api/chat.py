from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSessionResponse,
    ChatSessionDetailResponse,
    CreateSessionRequest
)
from app.services.chat_service import chat_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
def ask_question(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute grounded RAG pipeline for student question."""
    return chat_service.process_chat_message(
        db=db,
        user_id=current_user.id,
        question=data.question,
        session_id=data.session_id,
        category_filter=data.category_filter
    )

@router.get("/chats", response_model=List[ChatSessionResponse])
def get_user_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all chat sessions for the current authenticated user."""
    return chat_service.list_sessions(db, current_user.id)

@router.post("/chats", response_model=ChatSessionResponse)
def create_new_chat_session(
    data: CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Explicitly initialize a new chat session."""
    return chat_service.create_session(db, current_user.id, data.title or "New Conversation")

@router.get("/chats/{session_id}", response_model=ChatSessionDetailResponse)
def get_chat_session_details(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch conversation turn history for a session."""
    session = chat_service.get_session(db, session_id, current_user.id)
    return session

@router.delete("/chats/{session_id}")
def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chat conversation and its messages."""
    return chat_service.delete_session(db, session_id, current_user.id)
