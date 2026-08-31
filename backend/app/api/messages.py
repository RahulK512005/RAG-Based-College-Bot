from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.chat import ChatMessageResponse
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.chat_service import chat_service
from app.api.deps import get_current_user
from app.models.user import User
from app.models.message import ChatMessage

router = APIRouter(tags=["Messages"])

@router.get("/chats/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve message history for a conversation session."""
    session = chat_service.get_session(db, session_id, current_user.id)
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).order_by(ChatMessage.created_at.asc()).all()
    return messages

@router.post("/messages/{message_id}/feedback", response_model=FeedbackResponse)
def submit_answer_feedback(
    message_id: str,
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit positive (1) or negative (-1) rating and comment for an assistant message."""
    return chat_service.submit_feedback(
        db=db,
        message_id=message_id,
        user_id=current_user.id,
        rating=data.rating,
        comment=data.comment
    )
