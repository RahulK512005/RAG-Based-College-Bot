from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.session import ChatSession
from app.models.message import ChatMessage
from app.models.feedback import Feedback
from app.core.exceptions import AppCustomException
from app.rag.retriever import retriever
from app.rag.generator import rag_generator

class ChatService:
    @staticmethod
    def create_session(db: Session, user_id: str, title: str = "New Conversation") -> ChatSession:
        session = ChatSession(
            user_id=user_id,
            title=title.strip() or "New Conversation"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def list_sessions(db: Session, user_id: str) -> List[ChatSession]:
        return db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.updated_at.desc()).all()

    @staticmethod
    def get_session(db: Session, session_id: str, user_id: str) -> ChatSession:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        ).first()
        if not session:
            raise AppCustomException(status_code=404, code="SESSION_NOT_FOUND", message="Chat conversation not found.")
        return session

    @staticmethod
    def delete_session(db: Session, session_id: str, user_id: str) -> dict:
        session = ChatService.get_session(db, session_id, user_id)
        db.delete(session)
        db.commit()
        return {"success": True, "message": "Conversation deleted successfully."}

    @staticmethod
    def process_chat_message(
        db: Session,
        user_id: str,
        question: str,
        session_id: Optional[str] = None,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Get or create session
        if session_id:
            session = ChatService.get_session(db, session_id, user_id)
        else:
            # Generate short title from question
            auto_title = question[:35] + ("..." if len(question) > 35 else "")
            session = ChatService.create_session(db, user_id, auto_title)

        # 2. Persist User Question
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=question.strip(),
            sources=[]
        )
        db.add(user_msg)
        db.commit()

        # 3. Retrieve conversation history window
        past_messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).order_by(ChatMessage.created_at.asc()).all()

        history = [{"role": m.role, "content": m.content} for m in past_messages]

        # 4. RAG Retrieval Pipeline
        retrieval_result = retriever.retrieve(
            db=db,
            query_text=question,
            category_filter=category_filter
        )

        # 5. RAG Generation Pipeline
        gen_result = rag_generator.generate_answer(
            question=question,
            retrieval_result=retrieval_result,
            conversation_history=history[:-1] # exclude the newly added user message
        )

        # 6. Persist Assistant Response with Sources
        assistant_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=gen_result["answer"],
            sources=gen_result["sources"]
        )
        db.add(assistant_msg)
        
        # Update session title if needed
        if session.title == "New Conversation":
            session.title = question[:35] + ("..." if len(question) > 35 else "")

        db.commit()
        db.refresh(assistant_msg)

        return {
            "answer": gen_result["answer"],
            "session_id": session.id,
            "sources": gen_result["sources"],
            "message_id": assistant_msg.id,
            "is_unknown": gen_result["is_unknown"]
        }

    @staticmethod
    def submit_feedback(
        db: Session,
        message_id: str,
        user_id: str,
        rating: int,
        comment: Optional[str] = None
    ) -> Feedback:
        msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
        if not msg:
            raise AppCustomException(status_code=404, code="MESSAGE_NOT_FOUND", message="Message not found.")

        # Check existing feedback
        existing = db.query(Feedback).filter(
            Feedback.message_id == message_id,
            Feedback.user_id == user_id
        ).first()

        if existing:
            existing.rating = rating
            existing.comment = comment.strip() if comment else None
            db.commit()
            db.refresh(existing)
            return existing

        feedback = Feedback(
            message_id=message_id,
            user_id=user_id,
            rating=rating,
            comment=comment.strip() if comment else None
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

chat_service = ChatService()
