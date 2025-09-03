from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.assessment import CourseLevel, QuestionDifficulty, AssessmentStatus

# Subject schemas
class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    title: str
    level: CourseLevel
    description: Optional[str] = None
    url: Optional[str] = None

class CourseCreate(CourseBase):
    subject_id: int

class CourseResponse(CourseBase):
    id: int
    subject_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Question schemas
class QuestionBase(BaseModel):
    text: str
    options: List[str]
    difficulty: QuestionDifficulty

class QuestionCreate(QuestionBase):
    subject_id: int
    correct_index: int

class QuestionResponse(BaseModel):
    id: int
    subject_id: int
    text: str
    options: List[str]
    difficulty: QuestionDifficulty
    
    class Config:
        from_attributes = True

# Assessment session schemas
class AssessmentStartRequest(BaseModel):
    subject_ids: Optional[List[int]] = None
    num_questions_per_subject: Optional[int] = Field(default=10, ge=1, le=50)

class AssessmentStartResponse(BaseModel):
    session_id: int
    questions: List[QuestionResponse]

# Assessment answer schemas
class AssessmentAnswerRequest(BaseModel):
    question_id: int
    selected_index: int = Field(ge=0)

class AssessmentSubmitRequest(BaseModel):
    answers: List[AssessmentAnswerRequest]

# Assessment result schemas
class SubjectResult(BaseModel):
    subject_id: int
    subject_name: str
    percent_correct: float
    weighted_score: int
    level: CourseLevel
    recommended_courses: List[CourseResponse]

class AssessmentResult(BaseModel):
    session_id: int
    status: AssessmentStatus
    created_at: datetime
    results: List[SubjectResult]
    
    class Config:
        from_attributes = True

# Session info schema
class AssessmentSessionInfo(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    status: AssessmentStatus
    selected_subject_ids: List[int]
    num_questions_per_subject: int
    
    class Config:
        from_attributes = True
