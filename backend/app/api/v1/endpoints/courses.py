from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Any, Optional, Dict

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.assessment import Subject, Course, AssessmentQuestion, AssessmentSession, AssessmentAnswer, CourseLevel, AssessmentStatus
from app.services.recommendation_engine import RecommendationEngine
from app.schemas.assessment import CourseResponse

router = APIRouter()

@router.get("/recommend-courses/{user_id}")
async def recommend_courses_by_user_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get course recommendations for a specific user based on their assessment scores.
    
    This endpoint:
    1. Fetches user assessment scores per subject
    2. Maps scores to difficulty levels:
       - Score < 40% → Beginner courses
       - Score 40-70% → Intermediate courses  
       - Score > 70% → Advanced courses
    3. Returns recommended courses in the specified JSON format
    
    Args:
        user_id: ID of the user to get recommendations for
        
    Returns:
        JSON response with recommendations grouped by subject
    """
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Get latest assessment results
        latest_session = db.query(AssessmentSession).filter(
            AssessmentSession.user_id == user_id,
            AssessmentSession.status == AssessmentStatus.SUBMITTED
        ).order_by(AssessmentSession.created_at.desc()).first()
        
        if not latest_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No assessment results found for user {user_id}"
            )
        
        # Calculate scores per subject
        subject_scores = _calculate_subject_scores(db, latest_session)
        
        # Get recommendations based on scores
        recommendations = _get_recommendations_by_scores(db, subject_scores)
        
        return {
            "recommendations": recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

def _calculate_subject_scores(db: Session, session: AssessmentSession) -> Dict[str, float]:
    """
    Calculate percentage scores for each subject in the assessment session.
    """
    subject_scores = {}
    
    for subject_id in session.selected_subject_ids:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            continue
        
        # Get answers for this subject
        subject_answers = db.query(AssessmentAnswer).join(AssessmentQuestion).filter(
            AssessmentAnswer.session_id == session.id,
            AssessmentQuestion.subject_id == subject_id
        ).all()
        
        if not subject_answers:
            continue
        
        # Calculate percentage correct
        total_questions = len(subject_answers)
        correct_answers = [a for a in subject_answers if a.is_correct]
        percent_correct = (len(correct_answers) / total_questions) * 100
        
        subject_scores[subject.name] = round(percent_correct, 1)
    
    return subject_scores

def _get_recommendations_by_scores(db: Session, subject_scores: Dict[str, float]) -> Dict[str, List[str]]:
    """
    Get course recommendations based on subject scores.
    
    Score mapping:
    - < 40% → Beginner courses
    - 40-70% → Intermediate courses
    - > 70% → Advanced courses
    """
    recommendations = {}
    
    for subject_name, score in subject_scores.items():
        # Determine recommended level based on score
        if score < 40:
            recommended_level = CourseLevel.BEGINNER
        elif score <= 70:
            recommended_level = CourseLevel.INTERMEDIATE
        else:
            recommended_level = CourseLevel.ADVANCED
        
        # Get subject ID
        subject = db.query(Subject).filter(Subject.name == subject_name).first()
        if not subject:
            continue
        
        # Get courses at recommended level
        courses = db.query(Course).filter(
            Course.subject_id == subject.id,
            Course.level == recommended_level
        ).all()
        
        # If no courses at recommended level, try adjacent levels
        if not courses:
            if recommended_level == CourseLevel.BEGINNER:
                # Try intermediate
                courses = db.query(Course).filter(
                    Course.subject_id == subject.id,
                    Course.level == CourseLevel.INTERMEDIATE
                ).all()
            elif recommended_level == CourseLevel.ADVANCED:
                # Try intermediate
                courses = db.query(Course).filter(
                    Course.subject_id == subject.id,
                    Course.level == CourseLevel.INTERMEDIATE
                ).all()
            elif recommended_level == CourseLevel.INTERMEDIATE:
                # Try beginner
                courses = db.query(Course).filter(
                    Course.subject_id == subject.id,
                    Course.level == CourseLevel.BEGINNER
                ).all()
        
        # If still no courses, get any course for this subject
        if not courses:
            courses = db.query(Course).filter(Course.subject_id == subject.id).all()
        
        # Format course titles as clickable links
        course_titles = []
        for course in courses:
            if course.url:
                # Create clickable link with course name as text
                course_titles.append(f"[{course.title}]({course.url})")
            else:
                course_titles.append(course.title)
        
        recommendations[subject_name] = course_titles
    
    return recommendations

@router.get("/courses/recommendations/{student_id}")
async def get_course_recommendations(
    student_id: int,
    num_recommendations: int = Query(default=5, ge=1, le=20, description="Number of recommendations per subject"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get personalized course recommendations for a specific student based on their assessment performance.
    
    This endpoint analyzes the student's test results to:
    - Identify weakest subjects and areas
    - Recommend appropriate course levels (beginner/intermediate/advanced)
    - Provide personalized learning path suggestions
    
    Args:
        student_id: ID of the student to get recommendations for
        num_recommendations: Number of course recommendations to return per subject
        
    Returns:
        Dictionary containing:
        - student_id: ID of the student
        - student_name: Username of the student
        - recommendations: List of recommendations grouped by subject
            - subject: Subject name
            - weakness: Identified areas of weakness
            - performance_level: Overall performance level (weak/moderate/strong)
            - percent_correct: Percentage of correct answers
            - recommended_courses: List of recommended courses with details
    """
    try:
        # Check if current user has permission to view this student's recommendations
        # For now, allow any authenticated user to view any student's recommendations
        # In production, you might want to add role-based access control here
        
        # Initialize recommendation engine
        recommendation_engine = RecommendationEngine()
        
        # Get recommendations
        recommendations = recommendation_engine.get_course_recommendations(
            db=db,
            student_id=student_id,
            num_recommendations=num_recommendations
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No recommendations found for this student"
            )
        
        return recommendations
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

@router.get("/courses/recommendations/me")
async def get_my_course_recommendations(
    num_recommendations: int = Query(default=5, ge=1, le=20, description="Number of recommendations per subject"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get personalized course recommendations for the currently authenticated user.
    
    This is a convenience endpoint that calls the main recommendation endpoint
    with the current user's ID.
    """
    return await get_course_recommendations(
        student_id=current_user.id,
        num_recommendations=num_recommendations,
        current_user=current_user,
        db=db
    )

@router.get("/courses/recommendations/ml/{student_id}")
async def get_ml_course_recommendations(
    student_id: int,
    num_recommendations: int = Query(default=5, ge=1, le=20, description="Number of recommendations per subject"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get ML-powered course recommendations for a specific student.
    
    This endpoint uses the machine learning recommendation engine (future enhancement).
    Currently returns the same as the regular recommendation endpoint, but can be
    expanded to use collaborative filtering, content-based filtering, etc.
    """
    try:
        recommendation_engine = RecommendationEngine()
        
        recommendations = recommendation_engine.get_ml_recommendations(
            db=db,
            student_id=student_id,
            num_recommendations=num_recommendations
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No ML recommendations found for this student"
            )
        
        return recommendations
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating ML recommendations: {str(e)}"
        )
