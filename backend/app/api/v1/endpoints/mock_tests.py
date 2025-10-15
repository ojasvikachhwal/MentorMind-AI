from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from typing import List, Optional
from datetime import datetime, timedelta
import google.generativeai as genai
from app.core.config import settings
from app.core.database import get_db
from app.models.mock_test import (
    MockTest, MockTestQuestion, MockTestSession, 
    MockTestAnswer, MockTestAnalytics, MockTestStatus, MockTestSessionStatus
)
from app.schemas.mock_test import (
    MockTestCreate, MockTestUpdate, MockTestResponse, MockTestListResponse,
    MockTestQuestionCreate, MockTestQuestionUpdate, MockTestQuestionResponse,
    MockTestSessionCreate, MockTestSessionResponse, MockTestSessionListResponse,
    MockTestSubmission, MockTestResult, MockTestAnswerResponse,
    AIAnalysisRequest, AIAnalysisResponse, MockTestAnalyticsResponse
)
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

# Configure Gemini AI
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

# ==================== MOCK TEST MANAGEMENT (INSTRUCTOR) ====================

@router.post("/", response_model=MockTestResponse, status_code=status.HTTP_201_CREATED)
async def create_mock_test(
    mock_test: MockTestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new mock test with questions
    """
    try:
        # Validate that user is an instructor/admin
        if not hasattr(current_user, 'role') or current_user.role not in ['instructor', 'admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors and admins can create mock tests"
            )

        # Create mock test
        db_mock_test = MockTest(
            title=mock_test.title,
            description=mock_test.description,
            subject_id=mock_test.subject_id,
            instructor_id=current_user.id,
            time_limit_minutes=mock_test.time_limit_minutes,
            is_public=mock_test.is_public,
            status=MockTestStatus.DRAFT
        )
        
        db.add(db_mock_test)
        db.flush()  # Get the ID

        # Calculate total marks
        total_marks = 0

        # Add questions
        for question_data in mock_test.questions:
            db_question = MockTestQuestion(
                mock_test_id=db_mock_test.id,
                question_text=question_data.question_text,
                option_a=question_data.option_a,
                option_b=question_data.option_b,
                option_c=question_data.option_c,
                option_d=question_data.option_d,
                correct_option=question_data.correct_option,
                marks=question_data.marks,
                explanation=question_data.explanation,
                difficulty=question_data.difficulty
            )
            db.add(db_question)
            total_marks += question_data.marks

        # Update total marks
        db_mock_test.total_marks = total_marks
        
        db.commit()
        db.refresh(db_mock_test)

        return db_mock_test

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create mock test: {str(e)}"
        )

@router.get("/", response_model=MockTestListResponse)
async def get_mock_tests(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[MockTestStatus] = None,
    subject_id: Optional[int] = None,
    instructor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of mock tests with filtering and pagination
    """
    try:
        query = db.query(MockTest)
        
        # Apply filters
        if status:
            query = query.filter(MockTest.status == status)
        if subject_id:
            query = query.filter(MockTest.subject_id == subject_id)
        if instructor_id:
            query = query.filter(MockTest.instructor_id == instructor_id)
        
        # For students, only show public tests
        if hasattr(current_user, 'role') and current_user.role == 'student':
            query = query.filter(MockTest.is_public == True, MockTest.status == MockTestStatus.ACTIVE)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        tests = query.offset(offset).limit(size).all()
        
        # Add question count to each test
        for test in tests:
            test.question_count = len(test.questions)
        
        return MockTestListResponse(
            tests=tests,
            total=total,
            page=page,
            size=size
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch mock tests: {str(e)}"
        )

@router.get("/{test_id}", response_model=MockTestResponse)
async def get_mock_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific mock test by ID
    """
    try:
        test = db.query(MockTest).filter(MockTest.id == test_id).first()
        
        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mock test not found"
            )
        
        # Check permissions
        if (hasattr(current_user, 'role') and current_user.role == 'student' and 
            (not test.is_public or test.status != MockTestStatus.ACTIVE)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this mock test"
            )
        
        test.question_count = len(test.questions)
        return test

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch mock test: {str(e)}"
        )

@router.put("/{test_id}", response_model=MockTestResponse)
async def update_mock_test(
    test_id: int,
    mock_test_update: MockTestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a mock test (instructor only)
    """
    try:
        # Check permissions
        if not hasattr(current_user, 'role') or current_user.role not in ['instructor', 'admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors and admins can update mock tests"
            )

        test = db.query(MockTest).filter(MockTest.id == test_id).first()
        
        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mock test not found"
            )
        
        # Check ownership
        if test.instructor_id != current_user.id and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own mock tests"
            )

        # Update fields
        update_data = mock_test_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(test, field, value)
        
        test.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(test)
        
        test.question_count = len(test.questions)
        return test

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update mock test: {str(e)}"
        )

@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mock_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a mock test (instructor only)
    """
    try:
        # Check permissions
        if not hasattr(current_user, 'role') or current_user.role not in ['instructor', 'admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors and admins can delete mock tests"
            )

        test = db.query(MockTest).filter(MockTest.id == test_id).first()
        
        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mock test not found"
            )
        
        # Check ownership
        if test.instructor_id != current_user.id and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own mock tests"
            )

        db.delete(test)
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete mock test: {str(e)}"
        )

# ==================== QUESTION MANAGEMENT ====================

@router.post("/{test_id}/questions", response_model=MockTestQuestionResponse, status_code=status.HTTP_201_CREATED)
async def add_question_to_test(
    test_id: int,
    question: MockTestQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a question to an existing mock test
    """
    try:
        # Check permissions
        if not hasattr(current_user, 'role') or current_user.role not in ['instructor', 'admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors and admins can add questions"
            )

        test = db.query(MockTest).filter(MockTest.id == test_id).first()
        
        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mock test not found"
            )
        
        # Check ownership
        if test.instructor_id != current_user.id and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only add questions to your own mock tests"
            )

        # Create question
        db_question = MockTestQuestion(
            mock_test_id=test_id,
            question_text=question.question_text,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            correct_option=question.correct_option,
            marks=question.marks,
            explanation=question.explanation,
            difficulty=question.difficulty
        )
        
        db.add(db_question)
        
        # Update total marks
        test.total_marks += question.marks
        
        db.commit()
        db.refresh(db_question)
        
        return db_question

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add question: {str(e)}"
        )

# ==================== STUDENT TEST SESSIONS ====================

@router.post("/{test_id}/start", response_model=MockTestSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_mock_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Start a mock test session for a student
    """
    try:
        # Get the mock test
        test = db.query(MockTest).filter(
            and_(MockTest.id == test_id, MockTest.status == MockTestStatus.ACTIVE)
        ).first()
        
        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active mock test not found"
            )
        
        # Check if student already has an active session
        existing_session = db.query(MockTestSession).filter(
            and_(
                MockTestSession.mock_test_id == test_id,
                MockTestSession.student_id == current_user.id,
                MockTestSession.status.in_([MockTestSessionStatus.NOT_STARTED, MockTestSessionStatus.IN_PROGRESS])
            )
        ).first()
        
        if existing_session:
            return existing_session
        
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
        
        return session

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start mock test: {str(e)}"
        )

@router.post("/sessions/{session_id}/begin", response_model=MockTestSessionResponse)
async def begin_mock_test(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Begin a mock test session (start timer)
    """
    try:
        session = db.query(MockTestSession).filter(
            and_(
                MockTestSession.id == session_id,
                MockTestSession.student_id == current_user.id
            )
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
        db.refresh(session)
        
        return session

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to begin test session: {str(e)}"
        )

@router.post("/sessions/{session_id}/submit", response_model=MockTestResult)
async def submit_mock_test(
    session_id: int,
    submission: MockTestSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit answers for a mock test
    """
    try:
        session = db.query(MockTestSession).filter(
            and_(
                MockTestSession.id == session_id,
                MockTestSession.student_id == current_user.id
            )
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
                and_(
                    MockTestAnswer.session_id == session_id,
                    MockTestAnswer.question_id == answer_data.question_id
                )
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
        db.refresh(session)
        
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
            detail=f"Failed to submit mock test: {str(e)}"
        )

# ==================== AI ANALYSIS WITH GEMINI ====================

@router.post("/sessions/{session_id}/analyze", response_model=AIAnalysisResponse)
async def analyze_mock_test_with_ai(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze mock test results using Gemini AI
    """
    try:
        if not settings.GEMINI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI analysis service is not available"
            )
        
        # Get session with test and answers
        session = db.query(MockTestSession).filter(
            and_(
                MockTestSession.id == session_id,
                MockTestSession.student_id == current_user.id
            )
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test session not found"
            )
        
        if session.status != MockTestSessionStatus.SUBMITTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Test must be submitted before analysis"
            )
        
        # Get test details and answers
        test = db.query(MockTest).filter(MockTest.id == session.mock_test_id).first()
        answers = db.query(MockTestAnswer).filter(MockTestAnswer.session_id == session_id).all()
        questions = {q.id: q for q in test.questions}
        
        # Prepare data for AI analysis
        analysis_data = {
            "test_title": test.title,
            "subject_id": test.subject_id,
            "total_questions": len(questions),
            "correct_answers": session.correct_answers,
            "total_score": session.total_score,
            "total_marks": session.total_marks,
            "percentage": session.percentage,
            "time_taken_minutes": session.time_taken_minutes,
            "questions_analysis": []
        }
        
        # Add detailed question analysis
        for answer in answers:
            question = questions.get(answer.question_id)
            if question:
                analysis_data["questions_analysis"].append({
                    "question_text": question.question_text,
                    "difficulty": question.difficulty,
                    "correct_option": question.correct_option,
                    "selected_option": answer.selected_option,
                    "is_correct": answer.is_correct,
                    "marks_obtained": answer.marks_obtained,
                    "total_marks": question.marks,
                    "explanation": question.explanation
                })
        
        # Generate AI analysis prompt
        prompt = f"""
        As an AI educational analyst, please analyze this mock test performance and provide detailed insights:

        Test: {analysis_data['test_title']}
        Score: {analysis_data['total_score']}/{analysis_data['total_marks']} ({analysis_data['percentage']:.1f}%)
        Time Taken: {analysis_data['time_taken_minutes']} minutes
        Correct Answers: {analysis_data['correct_answers']}/{analysis_data['total_questions']}

        Question Analysis:
        {analysis_data['questions_analysis']}

        Please provide:
        1. Overall performance assessment
        2. Areas of strength (topics/concepts answered correctly)
        3. Areas for improvement (topics/concepts answered incorrectly)
        4. Specific recommendations for study and practice
        5. Performance summary (2-3 sentences)

        Format your response as JSON with these keys:
        - "overall_assessment": string
        - "strengths": array of strings
        - "weaknesses": array of strings  
        - "recommendations": array of strings
        - "performance_summary": string
        """
        
        # Get AI analysis
        response = model.generate_content(prompt)
        ai_analysis = response.text
        
        # Parse AI response (assuming it returns JSON)
        try:
            import json
            analysis_result = json.loads(ai_analysis)
        except:
            # Fallback if AI doesn't return proper JSON
            analysis_result = {
                "overall_assessment": "AI analysis completed",
                "strengths": ["Good attempt on the test"],
                "weaknesses": ["Some areas need improvement"],
                "recommendations": ["Continue practicing", "Review incorrect answers"],
                "performance_summary": f"Scored {analysis_data['percentage']:.1f}% on {analysis_data['test_title']}"
            }
        
        # Save analysis to database
        analytics = MockTestAnalytics(
            session_id=session_id,
            ai_analysis=analysis_result,
            strengths=analysis_result.get("strengths", []),
            weaknesses=analysis_result.get("weaknesses", []),
            recommendations=analysis_result.get("recommendations", []),
            performance_summary=analysis_result.get("performance_summary", "")
        )
        
        db.add(analytics)
        db.commit()
        
        return AIAnalysisResponse(
            analysis=analysis_result,
            strengths=analysis_result.get("strengths", []),
            weaknesses=analysis_result.get("weaknesses", []),
            recommendations=analysis_result.get("recommendations", []),
            performance_summary=analysis_result.get("performance_summary", "")
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze test with AI: {str(e)}"
        )

@router.get("/sessions/{session_id}/analytics", response_model=MockTestAnalyticsResponse)
async def get_mock_test_analytics(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI analysis results for a mock test session
    """
    try:
        # Verify session ownership
        session = db.query(MockTestSession).filter(
            and_(
                MockTestSession.id == session_id,
                MockTestSession.student_id == current_user.id
            )
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test session not found"
            )
        
        # Get analytics
        analytics = db.query(MockTestAnalytics).filter(
            MockTestAnalytics.session_id == session_id
        ).first()
        
        if not analytics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI analysis not found for this session"
            )
        
        return analytics

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch analytics: {str(e)}"
        )

# ==================== STUDENT SESSIONS LIST ====================

@router.get("/sessions/my", response_model=MockTestSessionListResponse)
async def get_my_mock_test_sessions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[MockTestSessionStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's mock test sessions
    """
    try:
        query = db.query(MockTestSession).filter(
            MockTestSession.student_id == current_user.id
        )
        
        if status:
            query = query.filter(MockTestSession.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        sessions = query.order_by(desc(MockTestSession.created_at)).offset(offset).limit(size).all()
        
        return MockTestSessionListResponse(
            sessions=sessions,
            total=total,
            page=page,
            size=size
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch sessions: {str(e)}"
        )
