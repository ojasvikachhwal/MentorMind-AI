from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Admin Authentication
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdminToken(BaseModel):
    access_token: str
    token_type: str
    admin: AdminResponse

# Student Management
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    assessment_score: Optional[float] = None
    assigned_courses: Optional[List[str]] = []

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    assessment_score: Optional[float] = None
    assigned_courses: Optional[List[str]] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Assessment Management
class AssessmentFilter(BaseModel):
    subject: Optional[str] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None

class AssessmentResponse(BaseModel):
    id: int
    student_name: str
    student_email: str
    subject: str
    score: float
    total_questions: int
    correct_answers: int
    completed_at: datetime
    
    class Config:
        from_attributes = True

# Course Management
class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CourseBase(BaseModel):
    subject: str
    level: CourseLevel
    title: str
    url: HttpUrl
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    subject: Optional[str] = None
    level: Optional[CourseLevel] = None
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Reports & Analytics
class SubjectAverageScore(BaseModel):
    subject: str
    average_score: float
    total_students: int
    min_score: float
    max_score: float

class StudentProgress(BaseModel):
    date: datetime
    subject: str
    score: float
    total_questions: int

class CoursePopularity(BaseModel):
    course_title: str
    subject: str
    level: str
    student_count: int
    average_score: float

# CSV Export
class CSVExportRequest(BaseModel):
    report_type: str  # "students", "assessments", "courses", "analytics"
    filters: Optional[dict] = None
