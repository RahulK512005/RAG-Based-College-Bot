from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.database.base import Base

# Import all models to ensure they register with Base.metadata
import app.models.user
import app.models.document
import app.models.chunk
import app.models.session
import app.models.message
import app.models.feedback

# Configure connect args for SQLite if used
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI dependency yielding a database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
