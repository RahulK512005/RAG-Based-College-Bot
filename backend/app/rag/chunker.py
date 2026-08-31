from typing import List, Dict, Any
from app.core.config import settings
from app.rag.cleaner import TextCleaner

class DocumentChunker:
    """Splits documents into semantic chunks preserving metadata and page boundaries."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    def chunk_document(
        self,
        pages_content: List[Dict[str, Any]],
        doc_metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Takes raw page objects and outputs list of chunk dictionaries with full metadata.
        """
        chunks = []
        global_chunk_index = 0

        for page in pages_content:
            raw_text = page.get("text", "")
            page_num = page.get("page_number", 1)
            cleaned_text = TextCleaner.clean_text(raw_text)

            if not cleaned_text:
                continue

            page_chunks = self._split_text_recursive(cleaned_text)

            for chunk_text in page_chunks:
                if not chunk_text.strip():
                    continue

                chunk_data = {
                    "content": chunk_text.strip(),
                    "page_number": page_num,
                    "chunk_index": global_chunk_index,
                    "metadata": {
                        "document_id": doc_metadata.get("document_id"),
                        "document_title": doc_metadata.get("title"),
                        "category": doc_metadata.get("category"),
                        "department": doc_metadata.get("department"),
                        "academic_year": doc_metadata.get("academic_year"),
                        "filename": doc_metadata.get("filename"),
                        "page_number": page_num,
                        "chunk_index": global_chunk_index
                    }
                }
                chunks.append(chunk_data)
                global_chunk_index += 1

        return chunks

    def _split_text_recursive(self, text: str) -> List[str]:
        """Split text by paragraphs, then sentences if necessary, respecting overlap."""
        if len(text) <= self.chunk_size:
            return [text]

        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If a single paragraph is longer than chunk_size, split by sentences
            if len(para) > self.chunk_size:
                sub_chunks = self._split_by_sentences(para)
                for sub in sub_chunks:
                    if len(current_chunk) + len(sub) + 1 <= self.chunk_size:
                        current_chunk = f"{current_chunk}\n{sub}".strip()
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = sub
            else:
                if len(current_chunk) + len(para) + 2 <= self.chunk_size:
                    current_chunk = f"{current_chunk}\n\n{para}".strip()
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                        # Add overlap from previous chunk
                        overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                        current_chunk = f"{overlap_text}\n\n{para}".strip()
                    else:
                        current_chunk = para

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _split_by_sentences(self, text: str) -> List[str]:
        """Split long paragraph by sentence boundaries."""
        sentences = [s.strip() for s in text.replace(". ", ".\n").split("\n") if s.strip()]
        chunks = []
        curr = ""

        for sent in sentences:
            if len(curr) + len(sent) + 1 <= self.chunk_size:
                curr = f"{curr} {sent}".strip()
            else:
                if curr:
                    chunks.append(curr)
                curr = sent

        if curr:
            chunks.append(curr)
        return chunks
