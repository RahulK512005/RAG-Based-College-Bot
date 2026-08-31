from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.document import DocumentStatsResponse
from app.services.document_service import document_service
from app.api.deps import require_admin
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics (Admin)"])

@router.get("/stats", response_model=DocumentStatsResponse)
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Aggregate statistics for Admin Dashboard metrics (Admin Only)."""
    return document_service.get_statistics(db)
