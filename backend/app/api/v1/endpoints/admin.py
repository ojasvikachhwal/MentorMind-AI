from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import csv
import io

from app.core.database import get_db
from app.core.admin_security import (
    authenticate_admin, create_access_token, get_current_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.schemas.admin import (
    AdminLogin, AdminToken, AdminResponse,
    StudentCreate, StudentUpdate, StudentResponse,
    AssessmentFilter, AssessmentResponse,
    CourseCreate, CourseUpdate, CourseResponse,
    SubjectAverageScore, StudentProgress, CoursePopularity,
    CSVExportRequest
)
from app.models.admin import Admin
from app.models.user import User
from app.models.assessment import AssessmentSession, AssessmentAnswer, AssessmentQuestion, Subject
from app.models.assessment import Course as AssessmentCourse

router = APIRouter()

# Admin Authentication
@router.post("/login", response_model=AdminToken)
async def admin_login(admin_credentials: AdminLogin, db: Session = Depends(get_db)):
    """Admin login endpoint."""
    admin = authenticate_admin(db, admin_credentials.username, admin_credentials.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin": admin
    }

@router.get("/me", response_model=AdminResponse)
async def get_admin_info(current_admin: Admin = Depends(get_current_admin)):
    """Get current admin information."""
    return current_admin

# Student Management
@router.get("/students", response_model=List[StudentResponse])
async def get_all_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all students with pagination and search."""
    query = db.query(User)
    
    if search:
        query = query.filter(
            User.username.contains(search) | User.email.contains(search)
        )
    
    students = query.offset(skip).limit(limit).all()
    
    # Convert to StudentResponse format
    student_responses = []
    for student in students:
        # Get assessment score (average of all sessions)
        avg_score = db.query(func.avg(AssessmentSession.score)).filter(
            AssessmentSession.user_id == student.id
        ).scalar()
        
        # Get assigned courses (simplified - could be enhanced)
        assigned_courses = []
        
        student_response = StudentResponse(
            id=student.id,
            name=student.username,
            email=student.email,
            assessment_score=float(avg_score) if avg_score else None,
            assigned_courses=assigned_courses,
            created_at=student.created_at
        )
        student_responses.append(student_response)
    
    return student_responses

@router.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a student by ID."""
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete related assessment sessions first
    db.query(AssessmentSession).filter(AssessmentSession.user_id == student_id).delete()
    
    # Delete the student
    db.delete(student)
    db.commit()
    
    return {"message": "Student deleted successfully"}

# Assessment Management
@router.get("/assessments", response_model=List[AssessmentResponse])
async def get_all_assessments(
    subject: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all assessment results with filtering."""
    query = db.query(AssessmentSession).join(User)
    
    if subject:
        query = query.join(Subject).filter(Subject.name == subject)
    
    if min_score is not None:
        query = query.filter(AssessmentSession.score >= min_score)
    
    if max_score is not None:
        query = query.filter(AssessmentSession.score <= max_score)
    
    assessments = query.offset(skip).limit(limit).all()
    
    assessment_responses = []
    for assessment in assessments:
        # Get total questions and correct answers
        total_questions = db.query(AssessmentAnswer).filter(
            AssessmentAnswer.session_id == assessment.id
        ).count()
        
        correct_answers = db.query(AssessmentAnswer).filter(
            AssessmentAnswer.session_id == assessment.id,
            AssessmentAnswer.is_correct == True
        ).count()
        
        # Get subject name
        subject_name = "Unknown"
        if assessment.selected_subject_ids:
            # This is simplified - in a real app you'd have proper subject relationships
            subject_name = "General"
        
        assessment_response = AssessmentResponse(
            id=assessment.id,
            student_name=assessment.user.username,
            student_email=assessment.user.email,
            subject=subject_name,
            score=assessment.score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            completed_at=assessment.completed_at or assessment.created_at
        )
        assessment_responses.append(assessment_response)
    
    return assessment_responses

# Course Management
@router.get("/courses", response_model=List[CourseResponse])
async def get_all_courses(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all courses."""
    courses = db.query(AssessmentCourse).all()
    return courses

@router.post("/courses", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new course."""
    # Check if subject exists, create if not
    subject = db.query(Subject).filter(Subject.name == course.subject).first()
    if not subject:
        subject = Subject(name=course.subject, description=f"Subject for {course.subject}")
        db.add(subject)
        db.commit()
        db.refresh(subject)
    
    db_course = AssessmentCourse(
        subject_id=subject.id,
        title=course.title,
        level=course.level,
        url=str(course.url),
        description=course.description
    )
    
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    return db_course

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update a course."""
    db_course = db.query(AssessmentCourse).filter(AssessmentCourse.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course_update.dict(exclude_unset=True)
    
    # Handle subject update
    if "subject" in update_data:
        subject = db.query(Subject).filter(Subject.name == update_data["subject"]).first()
        if not subject:
            subject = Subject(name=update_data["subject"], description=f"Subject for {update_data['subject']}")
            db.add(subject)
            db.commit()
            db.refresh(subject)
        update_data["subject_id"] = subject.id
        del update_data["subject"]
    
    # Handle URL update
    if "url" in update_data:
        update_data["url"] = str(update_data["url"])
    
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    
    return db_course

@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a course."""
    db_course = db.query(AssessmentCourse).filter(AssessmentCourse.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(db_course)
    db.commit()
    
    return {"message": "Course deleted successfully"}

# Reports & Analytics
@router.get("/reports/average-scores", response_model=List[SubjectAverageScore])
async def get_average_scores_by_subject(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get average scores per subject."""
    # This is a simplified version - in a real app you'd have proper subject relationships
    # For now, we'll return mock data structure
    subjects = ["Operating Systems", "Computer Networks", "OOPs", "DBMS", "Coding"]
    
    results = []
    for subject_name in subjects:
        # Mock data - replace with actual database queries
        avg_score = 75.0  # This would come from actual assessment data
        total_students = 25
        min_score = 45.0
        max_score = 95.0
        
        result = SubjectAverageScore(
            subject=subject_name,
            average_score=avg_score,
            total_students=total_students,
            min_score=min_score,
            max_score=max_score
        )
        results.append(result)
    
    return results

@router.get("/reports/student-progress/{student_id}", response_model=List[StudentProgress])
async def get_student_progress(
    student_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get individual student progress over time."""
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get assessment sessions for this student
    sessions = db.query(AssessmentSession).filter(
        AssessmentSession.user_id == student_id
    ).order_by(AssessmentSession.created_at).all()
    
    progress = []
    for session in sessions:
        progress_item = StudentProgress(
            date=session.created_at,
            subject="General",  # Simplified - would be actual subject
            score=session.score,
            total_questions=10  # Simplified - would be actual count
        )
        progress.append(progress_item)
    
    return progress

@router.get("/reports/course-popularity", response_model=List[CoursePopularity])
async def get_course_popularity(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get course popularity statistics."""
    courses = db.query(AssessmentCourse).all()
    
    popularity = []
    for course in courses:
        # Mock data - replace with actual database queries
        student_count = 15  # This would come from actual enrollment data
        average_score = 78.5  # This would come from actual assessment data
        
        popularity_item = CoursePopularity(
            course_title=course.title,
            subject=course.subject.name if course.subject else "Unknown",
            level=course.level.value,
            student_count=student_count,
            average_score=average_score
        )
        popularity.append(popularity_item)
    
    return popularity

# CSV Export
@router.post("/reports/export-csv")
async def export_csv_report(
    export_request: CSVExportRequest,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export data to CSV format."""
    
    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        
        if export_request.report_type == "students":
            # Export students data
            writer.writerow(["ID", "Name", "Email", "Assessment Score", "Created At"])
            students = db.query(User).all()
            for student in students:
                avg_score = db.query(func.avg(AssessmentSession.score)).filter(
                    AssessmentSession.user_id == student.id
                ).scalar()
                writer.writerow([
                    student.id,
                    student.username,
                    student.email,
                    f"{avg_score:.2f}" if avg_score else "N/A",
                    student.created_at.strftime("%Y-%m-%d %H:%M:%S")
                ])
        
        elif export_request.report_type == "assessments":
            # Export assessments data
            writer.writerow(["ID", "Student", "Score", "Completed At"])
            sessions = db.query(AssessmentSession).join(User).all()
            for session in sessions:
                writer.writerow([
                    session.id,
                    session.user.username,
                    f"{session.score:.2f}",
                    (session.completed_at or session.created_at).strftime("%Y-%m-%d %H:%M:%S")
                ])
        
        elif export_request.report_type == "courses":
            # Export courses data
            writer.writerow(["ID", "Title", "Subject", "Level", "URL", "Created At"])
            courses = db.query(AssessmentCourse).all()
            for course in courses:
                writer.writerow([
                    course.id,
                    course.title,
                    course.subject.name if course.subject else "Unknown",
                    course.level.value,
                    course.url,
                    course.created_at.strftime("%Y-%m-%d %H:%M:%S")
                ])
        
        output.seek(0)
        return output
    
    filename = f"{export_request.report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
