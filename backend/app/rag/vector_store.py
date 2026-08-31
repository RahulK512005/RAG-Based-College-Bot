import re
import math
import numpy as np
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.chunk import DocumentChunk
from app.models.document import Document

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it",
    "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on",
    "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so",
    "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself",
    "can", "tell", "give", "please", "know", "much", "many", "is", "are", "what", "how", "when", "where"
}

class VectorStore:
    """Hybrid Vector database interface supporting dense embeddings and BM25-style keyword search."""

    @staticmethod
    def store_chunks(db: Session, chunks_data: List[Dict[str, Any]]) -> List[DocumentChunk]:
        """Store chunk records with their embeddings in the database."""
        chunk_objects = []
        for item in chunks_data:
            chunk = DocumentChunk(
                document_id=item["metadata"]["document_id"],
                content=item["content"],
                embedding=item.get("embedding"),
                page_number=item.get("page_number", 1),
                section=item.get("section"),
                chunk_index=item.get("chunk_index", 0),
                chunk_metadata=item.get("metadata", {})
            )
            chunk_objects.append(chunk)

        db.add_all(chunk_objects)
        db.commit()
        for chunk in chunk_objects:
            db.refresh(chunk)
        return chunk_objects

    @staticmethod
    def similarity_search(
        db: Session,
        query_embedding: List[float],
        query_text: str = "",
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid retrieval (dense vector cosine similarity + lexical keyword scoring).
        """
        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm > 0:
            query_vec = query_vec / query_norm

        # Extract informative query keywords
        q_tokens = [w.lower().strip(".,!?;:\"'()[]{}#*-/\\") for w in query_text.split() if w.strip()]
        q_keywords = [w for w in q_tokens if w not in STOPWORDS and len(w) > 2]

        # Query all chunks from READY documents
        query = db.query(DocumentChunk, Document).join(
            Document, DocumentChunk.document_id == Document.id
        ).filter(Document.processing_status == "READY")

        if category_filter and category_filter.lower() != "all":
            query = query.filter(Document.category.ilike(f"%{category_filter}%"))

        results = query.all()
        scored_chunks = []

        for chunk, doc in results:
            if not chunk.embedding:
                continue

            chunk_vec = np.array(chunk.embedding, dtype=np.float32)
            chunk_norm = np.linalg.norm(chunk_vec)
            if chunk_norm > 0:
                chunk_vec = chunk_vec / chunk_norm

            # Dense cosine similarity
            dense_score = float(np.dot(query_vec, chunk_vec))
            dense_score = max(0.0, min(1.0, dense_score))

            # Lexical keyword match bonus
            content_lower = chunk.content.lower()
            doc_title_lower = doc.title.lower()
            
            keyword_score = 0.0
            if q_keywords:
                matched_count = 0
                for kw in q_keywords:
                    if kw in content_lower or kw in doc_title_lower:
                        matched_count += 1
                keyword_score = matched_count / len(q_keywords)

            # Combined hybrid score (70% dense vector + 30% lexical match)
            hybrid_score = 0.70 * dense_score + 0.30 * keyword_score
            hybrid_score = round(max(0.0, min(1.0, hybrid_score)), 4)

            scored_chunks.append({
                "chunk_id": chunk.id,
                "document_id": doc.id,
                "document_title": doc.title,
                "filename": doc.filename,
                "category": doc.category,
                "department": doc.department,
                "academic_year": doc.academic_year,
                "page_number": chunk.page_number or 1,
                "content": chunk.content,
                "similarity_score": hybrid_score,
                "metadata": chunk.chunk_metadata or {}
            })

        # Sort descending by similarity score
        scored_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)

        return scored_chunks[:top_k]

    @staticmethod
    def delete_document_chunks(db: Session, document_id: str):
        """Remove all chunks associated with a document."""
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
        db.commit()

vector_store = VectorStore()
