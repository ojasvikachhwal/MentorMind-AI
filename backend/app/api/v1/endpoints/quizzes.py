from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.quiz import Quiz, Question, QuizAttempt, QuizAnswer
from app.schemas.quiz import QuizCreate, QuizResponse, QuizAttemptCreate, QuizAttemptResponse, QuestionResponse
from app.ai.adaptive_quiz import AdaptiveQuizEngine

router = APIRouter()
adaptive_engine = AdaptiveQuizEngine()

@router.get("/available", response_model=List[QuizResponse])
async def get_available_quizzes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get available quizzes for the current user."""
    try:
        # Get all active quizzes
        quizzes = db.query(Quiz).filter(Quiz.is_active == True).all()
        
        # Get user's performance data for adaptive recommendations
        user_performance = {
            'overall_score': 0.5,  # Default value
            'topic_performances': {},
            'total_quizzes_taken': 0
        }
        
        # Get user's quiz attempts to calculate performance
        attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
        if attempts:
            total_score = sum(attempt.score or 0 for attempt in attempts)
            user_performance['overall_score'] = total_score / len(attempts)
            user_performance['total_quizzes_taken'] = len(attempts)
        
        # Add question count to each quiz
        for quiz in quizzes:
            quiz.question_count = db.query(Question).filter(Question.quiz_id == quiz.id).count()
        
        return quizzes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching quizzes: {str(e)}"
        )

@router.get("/topics")
async def get_quiz_topics(db: Session = Depends(get_db)) -> Any:
    """
    Get all available quiz topics.
    """
    topics = db.query(Quiz.topic).distinct().all()
    return [topic[0] for topic in topics]

@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific quiz by ID.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz

@router.get("/{quiz_id}/questions", response_model=List[QuestionResponse])
async def get_quiz_questions(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get questions for a specific quiz.
    """
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions found for this quiz"
        )
    return questions

@router.post("/{quiz_id}/start", response_model=dict)
async def start_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a quiz and get questions."""
    try:
        # Get quiz
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        # Get questions for this quiz
        questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions found for this quiz"
            )
        
        # Create quiz attempt
        attempt = QuizAttempt(
            user_id=current_user.id,
            quiz_id=quiz_id,
            total_questions=len(questions),
            started_at=datetime.utcnow()
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        
        # Return quiz data with questions (without correct answers)
        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "attempt_id": attempt.id,
            "questions": []
        }
        
        for question in questions:
            quiz_data["questions"].append({
                "id": question.id,
                "text": question.question_text,
                "options": question.options,
                "type": question.question_type
            })
        
        return quiz_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting quiz: {str(e)}"
        )

@router.post("/{quiz_id}/submit", response_model=dict)
async def submit_quiz(
    quiz_id: int,
    answers: QuizAttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get results."""
    try:
        # Get quiz attempt
        attempt = db.query(QuizAttempt).filter(
            QuizAttempt.id == answers.quiz_id,
            QuizAttempt.user_id == current_user.id
        ).first()
        
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz attempt not found"
            )
        
        # Get questions and correct answers
        questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
        
        correct_answers = 0
        total_questions = len(questions)
        
        # Process each answer
        for i, answer in enumerate(answers.answers):
            if i < len(questions):
                question = questions[i]
                is_correct = answer == question.correct_answer
                
                if is_correct:
                    correct_answers += 1
                
                # Save answer
                quiz_answer = QuizAnswer(
                    attempt_id=attempt.id,
                    question_id=question.id,
                    user_answer=str(answer),
                    is_correct=is_correct
                )
                db.add(quiz_answer)
        
        # Calculate score
        score = correct_answers / total_questions if total_questions > 0 else 0
        
        # Update attempt
        attempt.score = score
        attempt.correct_answers = correct_answers
        attempt.completed_at = datetime.utcnow()
        
        # Calculate time taken (if started_at is available)
        if attempt.started_at:
            time_taken = (attempt.completed_at - attempt.started_at).total_seconds()
            attempt.time_taken = int(time_taken)
        
        db.commit()
        
        # Update adaptive model
        user_performance = {
            'overall_score': score,
            'total_quizzes_taken': 1,
            'accuracy_rate': score
        }
        
        # Get adaptive difficulty adjustment
        difficulty_adjustment = adaptive_engine.predict_difficulty_adjustment(user_performance)
        attempt.difficulty_adjustment = difficulty_adjustment
        
        db.commit()
        
        return {
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "percentage": round(score * 100, 2),
            "difficulty_adjustment": difficulty_adjustment
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting quiz: {str(e)}"
        )

@router.get("/history", response_model=List[QuizAttemptResponse])
async def get_quiz_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's quiz history."""
    try:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == current_user.id
        ).order_by(QuizAttempt.completed_at.desc()).all()
        
        return attempts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching quiz history: {str(e)}"
        )

@router.get("/recommendations")
async def get_quiz_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get personalized quiz recommendations.
    """
    # This would typically get user performance from database
    # For now, return sample recommendations
    user_performance = {
        "overall_score": 0.7,
        "topic_performances": {
            "database": {"accuracy_rate": 0.8},
            "algorithms": {"accuracy_rate": 0.6}
        }
    }
    
    available_quizzes = db.query(Quiz).filter(Quiz.is_active == True).all()
    quiz_list = [
        {
            "id": quiz.id,
            "title": quiz.title,
            "topic": quiz.topic,
            "difficulty_level": quiz.difficulty_level,
            "description": quiz.description
        }
        for quiz in available_quizzes
    ]
    
    recommendations = adaptive_engine.get_quiz_recommendations(
        current_user.id, user_performance, quiz_list, 3
    )
    
    return recommendations

@router.get("/adaptive/{quiz_id}/next-question")
async def get_next_adaptive_question(
    quiz_id: int,
    current_difficulty: float = 1.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the next question based on adaptive difficulty.
    """
    # Get available questions
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions found for this quiz"
        )
    
    # Get user performance (this would come from database)
    user_performance = {
        "overall_score": 0.7,
        "current_streak": 3,
        "total_quizzes_taken": 5,
        "accuracy_rate": 0.75
    }
    
    # Convert questions to dict format for adaptive engine
    question_list = [
        {
            "id": q.id,
            "difficulty_score": q.difficulty_score,
            "topic": q.quiz.topic if q.quiz else "general"
        }
        for q in questions
    ]
    
    # Get next question using adaptive engine
    next_question = adaptive_engine.select_next_question(
        question_list, user_performance, current_difficulty
    )
    
    if not next_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No suitable question found"
        )
    
    # Get full question details
    question = db.query(Question).filter(Question.id == next_question["id"]).first()
    
    return question
