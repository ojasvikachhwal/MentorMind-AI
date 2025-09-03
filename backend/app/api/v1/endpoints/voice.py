from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Any, Optional
import tempfile
import os

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.voice_processor import VoiceProcessor
from app.ai.ai_tutor import AITutor

router = APIRouter()

# Initialize voice processor and AI tutor
voice_processor = VoiceProcessor()
ai_tutor = AITutor()

@router.post("/speech-to-text")
async def convert_speech_to_text(
    audio_file: UploadFile = File(...),
    language_code: str = "en-US",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Convert speech audio to text using Google Cloud Speech API.
    """
    try:
        # Validate file type
        if not audio_file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an audio file"
            )
        
        # Read audio data
        audio_data = await audio_file.read()
        
        # Validate audio format
        is_valid, message = voice_processor.validate_audio_format(audio_data)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Convert speech to text
        result = voice_processor.speech_to_text(audio_data, language_code)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return {
            "transcript": result["transcript"],
            "confidence": result["confidence"],
            "alternatives": result.get("alternatives", []),
            "language_code": language_code
        }
        
    except Exception as e:
        print(f"❌ Error in speech-to-text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing audio file"
        )

@router.post("/text-to-speech")
async def convert_text_to_speech(
    text: str,
    voice_name: str = "en-US-Standard-A",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Convert text to speech using Google Cloud Text-to-Speech API.
    """
    try:
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        # Convert text to speech
        audio_data = voice_processor.text_to_speech(text, voice_name)
        
        if not audio_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generating speech"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        # Return audio file
        return FileResponse(
            temp_file_path,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )
        
    except Exception as e:
        print(f"❌ Error in text-to-speech: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating speech"
        )

@router.post("/voice-question")
async def ask_question_via_voice(
    audio_file: UploadFile = File(...),
    language_code: str = "en-US",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Ask a question via voice and get AI tutor response.
    """
    try:
        # Convert speech to text
        audio_data = await audio_file.read()
        speech_result = voice_processor.speech_to_text(audio_data, language_code)
        
        if not speech_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Speech recognition failed: {speech_result['error']}"
            )
        
        question = speech_result["transcript"]
        
        # Get AI tutor response
        ai_response = ai_tutor.answer_question(question)
        
        # Convert response to speech
        response_text = f"Question: {question}. Answer: {ai_response['answer']}"
        audio_data = voice_processor.text_to_speech(response_text, "en-US-Standard-A")
        
        if not audio_data:
            # Return text response if speech generation fails
            return {
                "question": question,
                "response": ai_response,
                "audio_available": False
            }
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        return {
            "question": question,
            "response": ai_response,
            "audio_available": True,
            "audio_file": temp_file_path
        }
        
    except Exception as e:
        print(f"❌ Error in voice question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing voice question"
        )

@router.get("/supported-languages")
async def get_supported_languages() -> Any:
    """
    Get list of supported languages for speech recognition.
    """
    languages = voice_processor.get_supported_languages()
    return {"languages": languages}

@router.get("/available-voices")
async def get_available_voices() -> Any:
    """
    Get list of available voices for text-to-speech.
    """
    voices = voice_processor.get_available_voices()
    return {"voices": voices}

@router.post("/voice-quiz")
async def start_voice_quiz(
    topic: str,
    difficulty: str = "medium",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Start a voice-based quiz session.
    """
    try:
        # Generate practice question
        practice_questions = {
            "database": {
                "easy": {
                    "question": "What does SQL stand for?",
                    "answer": "Structured Query Language",
                    "explanation": "SQL is the standard language for relational database management systems."
                },
                "medium": {
                    "question": "What are the ACID properties in database transactions?",
                    "answer": "Atomicity, Consistency, Isolation, Durability",
                    "explanation": "ACID properties ensure reliable database transactions."
                },
                "hard": {
                    "question": "Explain the difference between 2NF and 3NF normalization.",
                    "answer": "2NF eliminates partial dependencies, 3NF eliminates transitive dependencies.",
                    "explanation": "Normalization reduces data redundancy and improves data integrity."
                }
            },
            "algorithms": {
                "easy": {
                    "question": "What is the time complexity of linear search?",
                    "answer": "O(n)",
                    "explanation": "Linear search checks each element one by one."
                },
                "medium": {
                    "question": "What is the space complexity of quicksort?",
                    "answer": "O(log n)",
                    "explanation": "Quicksort uses recursion, requiring stack space proportional to the depth of recursion."
                },
                "hard": {
                    "question": "Explain the concept of memoization in dynamic programming.",
                    "answer": "Memoization stores results of expensive function calls to avoid redundant calculations.",
                    "explanation": "It trades space for time by caching previously computed results."
                }
            }
        }
        
        if topic not in practice_questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        
        if difficulty not in practice_questions[topic]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Difficulty level not available for this topic"
            )
        
        question_data = practice_questions[topic][difficulty]
        
        # Convert question to speech
        question_audio = voice_processor.text_to_speech(
            question_data["question"], 
            "en-US-Standard-A"
        )
        
        if question_audio:
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(question_audio)
                temp_file_path = temp_file.name
            
            return {
                "quiz_session_id": f"voice_quiz_{current_user.id}_{topic}_{difficulty}",
                "question": question_data["question"],
                "topic": topic,
                "difficulty": difficulty,
                "question_audio": temp_file_path,
                "expected_answer": question_data["answer"],
                "explanation": question_data["explanation"]
            }
        else:
            return {
                "quiz_session_id": f"voice_quiz_{current_user.id}_{topic}_{difficulty}",
                "question": question_data["question"],
                "topic": topic,
                "difficulty": difficulty,
                "question_audio": None,
                "expected_answer": question_data["answer"],
                "explanation": question_data["explanation"]
            }
        
    except Exception as e:
        print(f"❌ Error starting voice quiz: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error starting voice quiz"
        )

@router.post("/voice-quiz/answer")
async def submit_voice_quiz_answer(
    quiz_session_id: str,
    audio_file: UploadFile = File(...),
    language_code: str = "en-US",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Submit answer for voice quiz via speech.
    """
    try:
        # Convert speech to text
        audio_data = await audio_file.read()
        speech_result = voice_processor.speech_to_text(audio_data, language_code)
        
        if not speech_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Speech recognition failed: {speech_result['error']}"
            )
        
        user_answer = speech_result["transcript"]
        
        # For now, return basic feedback
        # In a real implementation, this would check against the expected answer
        return {
            "quiz_session_id": quiz_session_id,
            "user_answer": user_answer,
            "confidence": speech_result["confidence"],
            "feedback": "Answer received successfully. Check your results.",
            "audio_available": False
        }
        
    except Exception as e:
        print(f"❌ Error submitting voice quiz answer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing voice answer"
        )

@router.get("/voice-settings")
async def get_voice_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's voice interaction settings.
    """
    # This would typically fetch from user preferences
    # For now, return default settings
    return {
        "preferred_language": "en-US",
        "preferred_voice": "en-US-Standard-A",
        "speech_rate": 1.0,
        "auto_play_audio": True,
        "voice_enabled": True
    }

@router.put("/voice-settings")
async def update_voice_settings(
    settings: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update user's voice interaction settings.
    """
    # This would typically save to user preferences
    # For now, just return success
    print(f"📝 Updated voice settings for {current_user.username}: {settings}")
    
    return {
        "message": "Voice settings updated successfully",
        "settings": settings
    }
