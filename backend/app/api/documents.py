from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.document import DocumentResponse, DocumentListResponse, DocumentUpdate
from app.services.document_service import document_service
from app.api.deps import require_admin
from app.models.user import User

router = APIRouter(prefix="/documents", tags=["Documents (Admin)"])

@router.post("", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form("General"),
    department: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Upload college document and trigger RAG ingestion pipeline (Admin Only)."""
    return document_service.upload_and_process(
        db=db,
        file=file,
        title=title,
        category=category,
        department=department,
        academic_year=academic_year,
        description=description,
        user_id=admin_user.id
    )

@router.get("", response_model=DocumentListResponse)
def list_documents(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """List uploaded college documents with status and search filtering (Admin Only)."""
    return document_service.list_documents(
        db=db,
        category=category,
        status=status,
        search=search,
        page=page,
        limit=limit
    )

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Get single document details (Admin Only)."""
    return document_service.get_document_by_id(db, document_id)

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    data: DocumentUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Update document metadata (Admin Only)."""
    doc = document_service.get_document_by_id(db, document_id)
    if data.title is not None:
        doc.title = data.title.strip()
    if data.category is not None:
        doc.category = data.category
    if data.department is not None:
        doc.department = data.department.strip() if data.department else None
    if data.academic_year is not None:
        doc.academic_year = data.academic_year.strip() if data.academic_year else None
    if data.description is not None:
        doc.description = data.description.strip() if data.description else None

    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Delete document and its corresponding vector chunks (Admin Only)."""
    return document_service.delete_document(db, document_id)

@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
def reprocess_document(
    document_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Re-extract text and re-generate embeddings for a document (Admin Only)."""
    return document_service.reprocess_document(db, document_id)
