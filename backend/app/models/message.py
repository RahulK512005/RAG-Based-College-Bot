import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False) # 'user' | 'assistant'
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True, default=[]) # List of { document_title, page, category, excerpt }
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    feedback = relationship("Feedback", back_populates="message", cascade="all, delete-orphan", uselist=False)
