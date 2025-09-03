from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.chat import ChatMessage, ChatSession
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatSessionResponse
from app.ai.ai_tutor import AITutor

router = APIRouter()
ai_tutor = AITutor()

@router.post("/chat", response_model=ChatMessageResponse)
async def send_message(
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to the AI tutor and get a response."""
    try:
        # Get or create chat session
        session = db.query(ChatSession).filter(
            ChatSession.user_id == current_user.id,
            ChatSession.is_active == True
        ).first()
        
        if not session:
            session = ChatSession(
                user_id=current_user.id,
                started_at=datetime.utcnow(),
                is_active=True
            )
            db.add(session)
            db.commit()
            db.refresh(session)
        
        # Save user message
        user_message = ChatMessage(
            session_id=session.id,
            message=message.message,
            sender="user",
            timestamp=datetime.utcnow()
        )
        db.add(user_message)
        db.commit()
        
        # Get AI response
        ai_response = ai_tutor.answer_question(message.message, current_user.id)
        
        # Save AI response
        ai_message = ChatMessage(
            session_id=session.id,
            message=ai_response,
            sender="ai",
            timestamp=datetime.utcnow()
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        return ChatMessageResponse(
            id=ai_message.id,
            message=ai_message.message,
            sender=ai_message.sender,
            timestamp=ai_message.timestamp
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )

@router.get("/chat/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for the current user."""
    try:
        # Get active chat session
        session = db.query(ChatSession).filter(
            ChatSession.user_id == current_user.id,
            ChatSession.is_active == True
        ).first()
        
        if not session:
            return []
        
        # Get messages for this session
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        return [
            ChatMessageResponse(
                id=msg.id,
                message=msg.message,
                sender=msg.sender,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching chat history: {str(e)}"
        )

@router.post("/chat/voice", response_model=ChatMessageResponse)
async def process_voice_message(
    audio_data: str,  # Base64 encoded audio
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process voice input and get AI response."""
    try:
        from app.ai.voice_processor import VoiceProcessor
        
        voice_processor = VoiceProcessor()
        
        # Convert speech to text
        text_message = voice_processor.speech_to_text(audio_data)
        
        if not text_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process voice input"
            )
        
        # Process the text message
        message = ChatMessageCreate(message=text_message)
        return await send_message(message, current_user, db)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing voice message: {str(e)}"
        )

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chat sessions for the current user."""
    try:
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == current_user.id
        ).order_by(ChatSession.started_at.desc()).all()
        
        return [
            ChatSessionResponse(
                id=session.id,
                started_at=session.started_at,
                ended_at=session.ended_at,
                is_active=session.is_active,
                message_count=db.query(ChatMessage).filter(
                    ChatMessage.session_id == session.id
                ).count()
            )
            for session in sessions
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching chat sessions: {str(e)}"
        )

@router.post("/sessions/{session_id}/end")
async def end_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End a chat session."""
    try:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        session.is_active = False
        session.ended_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Chat session ended successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ending chat session: {str(e)}"
        )

@router.get("/topics", response_model=List[str])
async def get_available_topics():
    """Get available topics for AI tutoring."""
    try:
        return [
            "Algorithms and Data Structures",
            "Database Systems",
            "Computer Networks",
            "Operating Systems",
            "Software Engineering",
            "Machine Learning",
            "Web Development",
            "Mobile Development",
            "Cybersecurity",
            "Cloud Computing"
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching topics: {str(e)}"
        )

@router.post("/explain-concept")
async def explain_concept(
    concept: str,
    topic: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a detailed explanation of a specific concept."""
    try:
        explanation = ai_tutor.explain_concept(concept, topic)
        
        return {
            "concept": concept,
            "topic": topic,
            "explanation": explanation,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error explaining concept: {str(e)}"
        )

@router.post("/practice-question")
async def generate_practice_question(
    topic: str,
    difficulty: str = "medium",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a practice question for a specific topic."""
    try:
        question = ai_tutor.generate_practice_question(topic, difficulty)
        
        return {
            "topic": topic,
            "difficulty": difficulty,
            "question": question,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating practice question: {str(e)}"
        )
