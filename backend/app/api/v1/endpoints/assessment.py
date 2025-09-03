from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.assessment import (
    SubjectResponse, AssessmentStartRequest, AssessmentStartResponse,
    AssessmentSubmitRequest, AssessmentResult
)
from app.services.assessment_service import AssessmentService

router = APIRouter()



@router.post("/assessment/start", response_model=AssessmentStartResponse)
async def start_assessment(
    request: AssessmentStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Start a new assessment session.
    
    - If subject_ids is null/empty, use all subjects
    - Creates session and samples questions per subject with difficulty mix
    """
    # Determine which subjects to use
    if not request.subject_ids:
        subject_ids = AssessmentService.get_all_subject_ids(db)
    else:
        subject_ids = request.subject_ids
    
    if not subject_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No subjects available for assessment"
        )
    
    # Create assessment session
    session = AssessmentService.create_assessment_session(
        db=db,
        user_id=current_user.id,
        subject_ids=subject_ids,
        num_questions_per_subject=request.num_questions_per_subject
    )
    
    # Get questions for the session
    questions = AssessmentService.get_questions_for_session(db, session)
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No questions available for selected subjects"
        )
    
    return AssessmentStartResponse(
        session_id=session.id,
        questions=questions
    )

@router.post("/assessment/{session_id}/submit", response_model=AssessmentResult)
async def submit_assessment(
    session_id: int,
    request: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Submit assessment answers and get results.
    
    - Saves answers and computes per-subject results
    - Maps scores to levels (beginner/intermediate/advanced)
    - Returns recommended courses for each subject
    """
    try:
        # Convert answers to the format expected by the service
        answers_data = [
            {
                "question_id": answer.question_id,
                "selected_index": answer.selected_index
            }
            for answer in request.answers
        ]
        
        result = AssessmentService.submit_assessment_answers(
            db=db,
            session_id=session_id,
            answers=answers_data
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/assessment/{session_id}/results", response_model=AssessmentResult)
async def get_assessment_results(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get assessment results for a specific session.
    """
    from app.models.assessment import AssessmentSession
    
    # Get the session
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found"
        )
    
    if session.status.value != "submitted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment session is not completed"
        )
    
    result = AssessmentService.calculate_assessment_results(db, session)
    return result

@router.get("/recommendations/latest", response_model=AssessmentResult)
async def get_latest_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get the latest assessment results and recommendations for the current user.
    """
    try:
        result = AssessmentService.get_latest_assessment_results(db, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
