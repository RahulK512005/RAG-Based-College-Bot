from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.rag.embeddings import embedding_service
from app.rag.vector_store import vector_store

class Retriever:
    """Orchestrates query embedding, semantic hybrid search, threshold filtering, and source metadata extraction."""

    def __init__(self):
        self.top_k = settings.TOP_K
        self.threshold = settings.SIMILARITY_THRESHOLD

    def retrieve(
        self,
        db: Session,
        query_text: str,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves relevant chunks for a user query.
        """
        # Generate query embedding
        query_embedding = embedding_service.get_embedding(query_text)

        # Hybrid Vector search
        candidates = vector_store.similarity_search(
            db=db,
            query_embedding=query_embedding,
            query_text=query_text,
            top_k=self.top_k,
            category_filter=category_filter
        )

        # Filter chunks by similarity threshold
        relevant_chunks = [c for c in candidates if c["similarity_score"] >= self.threshold]

        # Extract structured source citations (deduplicated by document + page)
        sources = []
        seen_citations = set()

        for chunk in relevant_chunks:
            citation_key = f"{chunk['document_id']}_{chunk['page_number']}"
            
            clean_excerpt = chunk["content"][:250].strip() + ("..." if len(chunk["content"]) > 250 else "")
            
            source_item = {
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "filename": chunk["filename"],
                "page_number": chunk["page_number"],
                "category": chunk["category"],
                "department": chunk.get("department"),
                "similarity_score": chunk["similarity_score"],
                "excerpt": clean_excerpt
            }

            if citation_key not in seen_citations:
                seen_citations.add(citation_key)
                sources.append(source_item)

        max_score = candidates[0]["similarity_score"] if candidates else 0.0
        has_relevant = len(relevant_chunks) > 0

        return {
            "query": query_text,
            "chunks": relevant_chunks,
            "sources": sources,
            "has_relevant_context": has_relevant,
            "max_score": max_score
        }

retriever = Retriever()
