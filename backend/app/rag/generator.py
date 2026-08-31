from typing import List, Dict, Any, Optional
import requests
from app.core.config import settings

UNKNOWN_REFUSAL_MESSAGE = (
    "I couldn't find reliable information about that in the college knowledge base.\n\n"
    "Please try rephrasing your question or contact the relevant college department."
)

SYSTEM_PROMPT = """You are an official AI College Information Assistant.

Your job is to answer student questions using ONLY the provided college knowledge-base context below.

STRICT RULES:
1. Answer ONLY using facts directly stated in the RETRIEVED CONTEXT.
2. Do NOT invent or assume:
   - Fees or payment amounts
   - Admission criteria, cutoffs, or deadlines
   - Examination dates or schedules
   - Hostel rules or room allocation details
   - Placement packages or recruiting companies
   - Scholarship eligibility or amounts
   - College policies or contact details
3. If the retrieved context does NOT contain sufficient information to answer the question truthfully and completely, respond with:
   "I couldn't find reliable information about that in the college knowledge base. Please try rephrasing your question or contact the relevant college department."
4. Be clear, professional, concise, and well-structured (use bullet points where appropriate).
5. Mention the source document name and page number when citing specific rules or figures.
"""

class RAGGenerator:
    """Generates grounded answers from retrieved context while strictly preventing hallucinations."""

    def generate_answer(
        self,
        question: str,
        retrieval_result: Dict[str, Any],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Takes question and retrieved chunks, returns grounded answer.
        """
        # If no relevant chunks were retrieved or max similarity is below threshold
        if not retrieval_result.get("has_relevant_context") or not retrieval_result.get("chunks"):
            return {
                "answer": UNKNOWN_REFUSAL_MESSAGE,
                "sources": [],
                "is_unknown": True
            }

        chunks = retrieval_result["chunks"]
        sources = retrieval_result["sources"]

        # Build structured context block
        context_blocks = []
        for c in chunks:
            block = (
                f"[Document: {c['document_title']}]\n"
                f"[Page: {c['page_number']}]\n"
                f"[Category: {c['category']}]\n"
                f"{c['content']}"
            )
            context_blocks.append(block)

        full_context = "\n\n---\n\n".join(context_blocks)

        # 1. Try LLM API (NVIDIA Nemotron / OpenAI / OpenRouter)
        if settings.LLM_API_KEY and not settings.LLM_API_KEY.startswith("mock"):
            llm_response = self._call_llm_api(question, full_context, conversation_history)
            if llm_response:
                return {
                    "answer": llm_response,
                    "sources": sources,
                    "is_unknown": False
                }

        # 2. Local Grounded Synthesizer (Fallback when API key is not configured)
        synthesized_answer = self._synthesize_grounded_answer(question, chunks)
        return {
            "answer": synthesized_answer,
            "sources": sources,
            "is_unknown": False
        }

    def _call_llm_api(
        self,
        question: str,
        context: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """Invoke external LLM API via OpenAI-compatible endpoint."""
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            # Add recent conversation history if provided
            if history:
                for h in history[-settings.MAX_HISTORY_MESSAGES:]:
                    messages.append({"role": h["role"], "content": h["content"]})

            # Add current user prompt with retrieved context
            user_prompt = f"RETRIEVED CONTEXT:\n{context}\n\nUSER QUESTION:\n{question}"
            messages.append({"role": "user", "content": user_prompt})

            headers = {
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json"
            }

            # Determine endpoint URL
            base_url = settings.LLM_BASE_URL.rstrip("/") if settings.LLM_BASE_URL else "https://integrate.api.nvidia.com/v1"
            endpoint = f"{base_url}/chat/completions"

            response = requests.post(
                endpoint,
                headers=headers,
                json={
                    "model": settings.LLM_MODEL,
                    "messages": messages,
                    "temperature": 0.1, # Low temperature to enforce deterministic grounding
                    "max_tokens": 1024
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                if content:
                    return content.strip()
            else:
                print(f"⚠️ LLM API returned status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"⚠️ LLM API call error: {e}. Utilizing built-in grounded synthesizer.")
        return None

    def _synthesize_grounded_answer(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        """
        Deterministic, grounded extraction from retrieved chunks.
        Extracts relevant sentences and formats them with source references.
        """
        q_words = set(question.lower().replace("?", "").split())
        matched_sentences = []

        for chunk in chunks:
            doc_title = chunk["document_title"]
            page = chunk["page_number"]
            content = chunk["content"]
            sentences = [s.strip() for s in content.replace("\n", " ").split(".") if len(s.strip()) > 15]

            for s in sentences:
                s_lower = s.lower()
                overlap = sum(1 for w in q_words if w in s_lower and len(w) > 2)
                if overlap > 0:
                    matched_sentences.append((overlap, f"{s}.", doc_title, page))

        if not matched_sentences:
            top = chunks[0]
            return f"Based on **{top['document_title']}** (Page {top['page_number']}):\n\n{top['content']}"

        matched_sentences.sort(key=lambda x: x[0], reverse=True)
        top_sentences = matched_sentences[:4]

        doc_grouped = {}
        for _, sent, doc, pg in top_sentences:
            key = f"{doc} (Page {pg})"
            if key not in doc_grouped:
                doc_grouped[key] = []
            if sent not in doc_grouped[key]:
                doc_grouped[key].append(sent)

        response_parts = ["According to official college documentation:\n"]
        for source_header, sents in doc_grouped.items():
            response_parts.append(f"**{source_header}**:")
            for s in sents:
                response_parts.append(f"- {s}")
            response_parts.append("")

        return "\n".join(response_parts).strip()

rag_generator = RAGGenerator()
