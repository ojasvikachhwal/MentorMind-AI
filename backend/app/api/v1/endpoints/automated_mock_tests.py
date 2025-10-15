from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.assessment import Subject
from app.models.student_progress import StudentSubjectProgress
from app.models.mock_test import MockTest, MockTestSession, MockTestAnswer, MockTestSessionStatus
from app.schemas.mock_test import MockTestResponse, MockTestSubmission, MockTestResult
from app.models.user import User
from app.core.security import get_current_user
from app.services.automated_mock_test_service import AutomatedMockTestService
from datetime import datetime

router = APIRouter()

# Initialize the automated test service
automated_service = AutomatedMockTestService()

@router.get("/subjects", response_model=List[dict])
async def get_available_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of available subjects for automated mock tests
    """
    try:
        subjects = db.query(Subject).filter(Subject.is_active == True).all()
        return [
            {
                "id": subject.id,
                "name": subject.name,
                "description": subject.description
            }
            for subject in subjects
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch subjects: {str(e)}"
        )

@router.get("/subjects/{subject_id}/progress")
async def get_student_progress(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get student's progress in a specific subject
    """
    try:
        progress = db.query(StudentSubjectProgress).filter(
            StudentSubjectProgress.student_id == current_user.id,
            StudentSubjectProgress.subject_id == subject_id
        ).first()
        
        if not progress:
            return {
                "subject_id": subject_id,
                "progress_percentage": 0.0,
                "total_tests_taken": 0,
                "average_score": 0.0,
                "best_score": 0.0,
                "last_test_date": None
            }
        
        return {
            "subject_id": subject_id,
            "progress_percentage": progress.current_progress_percentage,
            "total_tests_taken": progress.total_tests_taken,
            "average_score": progress.average_score,
            "best_score": progress.best_score,
            "last_test_date": progress.last_test_date
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch progress: {str(e)}"
        )

@router.post("/subjects/{subject_id}/generate", response_model=MockTestResponse)
async def generate_automated_test(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate an automated mock test for a student based on their progress
    """
    try:
        # Check if subject exists
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found"
            )
        
        # Generate the test
        mock_test = automated_service.generate_mock_test(
            subject_id=subject_id,
            student_id=current_user.id,
            db=db
        )
        
        if not mock_test:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate test"
            )
        
        # Add question count for response
        mock_test.question_count = len(mock_test.questions)
        
        return mock_test
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate test: {str(e)}"
        )

@router.post("/tests/{test_id}/start", response_model=dict)
async def start_automated_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Start an automated mock test session
    """
    try:
        # Get the test
        test = db.query(MockTest).filter(MockTest.id == test_id).first()
        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test not found"
            )
        
        # Check if student already has an active session
        existing_session = db.query(MockTestSession).filter(
            MockTestSession.mock_test_id == test_id,
            MockTestSession.student_id == current_user.id,
            MockTestSession.status.in_([MockTestSessionStatus.NOT_STARTED, MockTestSessionStatus.IN_PROGRESS])
        ).first()
        
        if existing_session:
            return {
                "session_id": existing_session.id,
                "test_id": test_id,
                "status": existing_session.status,
                "message": "Existing session found"
            }
        
        # Create new session
        session = MockTestSession(
            mock_test_id=test_id,
            student_id=current_user.id,
            status=MockTestSessionStatus.NOT_STARTED,
            total_marks=test.total_marks
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "session_id": session.id,
            "test_id": test_id,
            "status": session.status,
            "message": "Session created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start test: {str(e)}"
        )

@router.post("/sessions/{session_id}/begin", response_model=dict)
async def begin_automated_test(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Begin an automated test session (start timer)
    """
    try:
        session = db.query(MockTestSession).filter(
            MockTestSession.id == session_id,
            MockTestSession.student_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test session not found"
            )
        
        if session.status != MockTestSessionStatus.NOT_STARTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Test session has already been started"
            )
        
        # Update session status and start time
        session.status = MockTestSessionStatus.IN_PROGRESS
        session.started_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "session_id": session_id,
            "status": session.status,
            "started_at": session.started_at,
            "message": "Test started successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to begin test: {str(e)}"
        )

@router.post("/sessions/{session_id}/submit", response_model=MockTestResult)
async def submit_automated_test(
    session_id: int,
    submission: MockTestSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit answers for an automated mock test
    """
    try:
        session = db.query(MockTestSession).filter(
            MockTestSession.id == session_id,
            MockTestSession.student_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test session not found"
            )
        
        if session.status not in [MockTestSessionStatus.NOT_STARTED, MockTestSessionStatus.IN_PROGRESS]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Test session has already been submitted"
            )
        
        # Get test questions
        test = db.query(MockTest).filter(MockTest.id == session.mock_test_id).first()
        questions = {q.id: q for q in test.questions}
        
        # Process answers
        total_score = 0.0
        correct_answers = 0
        
        for answer_data in submission.answers:
            question = questions.get(answer_data.question_id)
            if not question:
                continue
            
            # Check if answer is correct
            is_correct = answer_data.selected_option == question.correct_option
            marks_obtained = question.marks if is_correct else 0.0
            
            if is_correct:
                correct_answers += 1
                total_score += marks_obtained
            
            # Create or update answer record
            existing_answer = db.query(MockTestAnswer).filter(
                MockTestAnswer.session_id == session_id,
                MockTestAnswer.question_id == answer_data.question_id
            ).first()
            
            if existing_answer:
                existing_answer.selected_option = answer_data.selected_option
                existing_answer.is_correct = is_correct
                existing_answer.marks_obtained = marks_obtained
            else:
                answer = MockTestAnswer(
                    session_id=session_id,
                    question_id=answer_data.question_id,
                    selected_option=answer_data.selected_option,
                    is_correct=is_correct,
                    marks_obtained=marks_obtained
                )
                db.add(answer)
        
        # Update session
        session.status = MockTestSessionStatus.SUBMITTED
        session.submitted_at = datetime.utcnow()
        session.total_score = total_score
        session.correct_answers = correct_answers
        
        # Calculate percentage
        if session.total_marks > 0:
            session.percentage = (total_score / session.total_marks) * 100
        
        # Calculate time taken
        if session.started_at:
            time_taken = session.submitted_at - session.started_at
            session.time_taken_minutes = int(time_taken.total_seconds() / 60)
        
        db.commit()
        
        # Update student progress
        automated_service.update_student_progress(
            student_id=current_user.id,
            subject_id=test.subject_id,
            test_score=total_score,
            total_marks=session.total_marks,
            db=db
        )
        
        # Get all answers for response
        answers = db.query(MockTestAnswer).filter(MockTestAnswer.session_id == session_id).all()
        
        return MockTestResult(
            session_id=session.id,
            total_score=session.total_score,
            total_marks=session.total_marks,
            percentage=session.percentage,
            correct_answers=correct_answers,
            total_questions=len(questions),
            time_taken_minutes=session.time_taken_minutes,
            submitted_at=session.submitted_at,
            answers=answers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit test: {str(e)}"
        )

@router.post("/sessions/{session_id}/evaluate")
async def evaluate_automated_test(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Evaluate test performance using AI
    """
    try:
        # Verify session ownership
        session = db.query(MockTestSession).filter(
            MockTestSession.id == session_id,
            MockTestSession.student_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test session not found"
            )
        
        if session.status != MockTestSessionStatus.SUBMITTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Test must be submitted before evaluation"
            )
        
        # Get AI evaluation
        evaluation = automated_service.evaluate_test_with_ai(
            test_session_id=session_id,
            db=db
        )
        
        return evaluation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to evaluate test: {str(e)}"
        )

@router.get("/progress/all")
async def get_all_student_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get student's progress across all subjects
    """
    try:
        progress_records = db.query(StudentSubjectProgress).filter(
            StudentSubjectProgress.student_id == current_user.id
        ).all()
        
        progress_data = []
        for progress in progress_records:
            progress_data.append({
                "subject_id": progress.subject_id,
                "subject_name": progress.subject.name,
                "progress_percentage": progress.current_progress_percentage,
                "total_tests_taken": progress.total_tests_taken,
                "average_score": progress.average_score,
                "best_score": progress.best_score,
                "last_test_date": progress.last_test_date
            })
        
        return progress_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch progress: {str(e)}"
        )
