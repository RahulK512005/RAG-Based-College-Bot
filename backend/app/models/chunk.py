import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True) # Serialized float vector list
    page_number = Column(Integer, nullable=True)
    section = Column(String(255), nullable=True)
    chunk_index = Column(Integer, nullable=False)
    chunk_metadata = Column(JSON, nullable=True, default={})
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    document = relationship("Document", back_populates="chunks")
