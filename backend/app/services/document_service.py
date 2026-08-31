import os
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.document import Document
from app.models.chunk import DocumentChunk
from app.models.user import User
from app.models.message import ChatMessage
from app.core.config import settings
from app.core.exceptions import AppCustomException
from app.rag.extractors import DocumentExtractor
from app.rag.chunker import DocumentChunker
from app.rag.embeddings import embedding_service
from app.rag.vector_store import vector_store

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md", ".csv"}

class DocumentService:
    @staticmethod
    def upload_and_process(
        db: Session,
        file: UploadFile,
        title: str,
        category: str,
        department: Optional[str],
        academic_year: Optional[str],
        description: Optional[str],
        user_id: str
    ) -> Document:
        """Saves file to disk, creates database record, and runs the RAG ingestion pipeline."""
        filename = file.filename or "uploaded_document"
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise AppCustomException(
                status_code=400,
                code="INVALID_FILE_TYPE",
                message=f"Unsupported file format '{ext}'. Allowed types: PDF, DOCX, TXT."
            )

        # Create upload directory
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        storage_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Write uploaded file to disk
        try:
            with open(storage_path, "wb") as f:
                content = file.file.read()
                if len(content) == 0:
                    raise AppCustomException(status_code=400, code="EMPTY_FILE", message="Uploaded file is empty.")
                f.write(content)
        except Exception as e:
            raise AppCustomException(status_code=500, code="FILE_SAVE_ERROR", message="Failed to store uploaded file.")

        # Create Document record with status PROCESSING
        doc = Document(
            title=title.strip(),
            filename=filename,
            category=category or "General",
            department=department.strip() if department else None,
            academic_year=academic_year.strip() if academic_year else None,
            description=description.strip() if description else None,
            storage_path=storage_path,
            processing_status="PROCESSING",
            uploaded_by=user_id
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # Execute Document Processing Pipeline
        try:
            DocumentService._execute_ingestion(db, doc)
        except Exception as err:
            doc.processing_status = "FAILED"
            doc.processing_error = str(err)
            db.commit()
            print(f"❌ Document Ingestion Error for {doc.id}: {err}")

        return doc

    @staticmethod
    def _execute_ingestion(db: Session, doc: Document):
        """Internal worker executing extraction, chunking, embedding, and vector storage."""
        # 1. Extract text
        pages_content = DocumentExtractor.extract_from_file(doc.storage_path, doc.filename)

        # 2. Chunk text
        chunker = DocumentChunker()
        doc_metadata = {
            "document_id": doc.id,
            "title": doc.title,
            "category": doc.category,
            "department": doc.department,
            "academic_year": doc.academic_year,
            "filename": doc.filename
        }
        chunks_data = chunker.chunk_document(pages_content, doc_metadata)

        if not chunks_data:
            raise ValueError("Document did not yield any valid text chunks.")

        # 3. Generate Embeddings
        chunk_texts = [c["content"] for c in chunks_data]
        embeddings = embedding_service.get_embeddings(chunk_texts)

        for idx, emb in enumerate(embeddings):
            chunks_data[idx]["embedding"] = emb

        # 4. Remove any existing chunks if reprocessing
        vector_store.delete_document_chunks(db, doc.id)

        # 5. Store chunks in database / vector index
        vector_store.store_chunks(db, chunks_data)

        # 6. Update Document status to READY
        doc.processing_status = "READY"
        doc.processing_error = None
        db.commit()
        db.refresh(doc)

    @staticmethod
    def list_documents(
        db: Session,
        category: Optional[str] = None,
        search: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> Dict[str, Any]:
        query = db.query(Document)

        if category and category.lower() != "all":
            query = query.filter(Document.category == category)
        if status and status.lower() != "all":
            query = query.filter(Document.processing_status == status)
        if search:
            query = query.filter(
                (Document.title.ilike(f"%{search}%")) |
                (Document.filename.ilike(f"%{search}%")) |
                (Document.category.ilike(f"%{search}%"))
            )

        total = query.count()
        documents = query.order_by(Document.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

        # Attach chunk counts
        doc_list = []
        for doc in documents:
            chunk_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).count()
            doc_dict = {
                "id": doc.id,
                "title": doc.title,
                "filename": doc.filename,
                "category": doc.category,
                "department": doc.department,
                "academic_year": doc.academic_year,
                "description": doc.description,
                "processing_status": doc.processing_status,
                "processing_error": doc.processing_error,
                "uploaded_by": doc.uploaded_by,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at,
                "chunk_count": chunk_count
            }
            doc_list.append(doc_dict)

        return {"documents": doc_list, "total": total}

    @staticmethod
    def get_document_by_id(db: Session, doc_id: str) -> Document:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            raise AppCustomException(status_code=404, code="DOCUMENT_NOT_FOUND", message="Document not found.")
        return doc

    @staticmethod
    def delete_document(db: Session, doc_id: str) -> dict:
        """Cascading deletion of chunks, file storage, and DB document."""
        doc = DocumentService.get_document_by_id(db, doc_id)

        # 1. Delete associated vector chunks
        vector_store.delete_document_chunks(db, doc_id)

        # 2. Delete local stored file
        if os.path.exists(doc.storage_path):
            try:
                os.remove(doc.storage_path)
            except Exception as e:
                print(f"⚠️ Could not delete local file {doc.storage_path}: {e}")

        # 3. Delete Document record
        db.delete(doc)
        db.commit()

        return {"success": True, "message": "Document and associated vectors deleted successfully."}

    @staticmethod
    def reprocess_document(db: Session, doc_id: str) -> Document:
        """Reprocess an existing document file through the chunking and embedding pipeline."""
        doc = DocumentService.get_document_by_id(db, doc_id)

        if not os.path.exists(doc.storage_path):
            raise AppCustomException(
                status_code=400,
                code="FILE_NOT_FOUND",
                message="Underlying document file is missing from storage."
            )

        doc.processing_status = "PROCESSING"
        doc.processing_error = None
        db.commit()

        try:
            DocumentService._execute_ingestion(db, doc)
        except Exception as err:
            doc.processing_status = "FAILED"
            doc.processing_error = str(err)
            db.commit()
            raise AppCustomException(status_code=500, code="REPROCESSING_FAILED", message=str(err))

        return doc

    @staticmethod
    def get_statistics(db: Session) -> Dict[str, int]:
        """Aggregate system statistics for admin dashboard."""
        total_docs = db.query(Document).count()
        ready_docs = db.query(Document).filter(Document.processing_status == "READY").count()
        proc_docs = db.query(Document).filter(Document.processing_status == "PROCESSING").count()
        failed_docs = db.query(Document).filter(Document.processing_status == "FAILED").count()
        total_chunks = db.query(DocumentChunk).count()
        total_users = db.query(User).count()
        total_questions = db.query(ChatMessage).filter(ChatMessage.role == "user").count()

        return {
            "total_documents": total_docs,
            "ready_documents": ready_docs,
            "processing_documents": proc_docs,
            "failed_documents": failed_docs,
            "total_chunks": total_chunks,
            "total_users": total_users,
            "total_questions": total_questions
        }

document_service = DocumentService()
