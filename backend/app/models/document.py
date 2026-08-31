import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, default="General")
    department = Column(String(100), nullable=True)
    academic_year = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    storage_path = Column(String(500), nullable=False)
    processing_status = Column(String(20), default="UPLOADED", nullable=False) # 'UPLOADED', 'PROCESSING', 'READY', 'FAILED'
    processing_error = Column(Text, nullable=True)
    uploaded_by = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    uploader = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
