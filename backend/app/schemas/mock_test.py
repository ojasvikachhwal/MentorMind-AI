from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class MockTestStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"

class MockTestSessionStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"

class QuestionOption(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

# Base schemas
class MockTestQuestionBase(BaseModel):
    question_text: str = Field(..., min_length=10, max_length=1000)
    option_a: str = Field(..., min_length=1, max_length=500)
    option_b: str = Field(..., min_length=1, max_length=500)
    option_c: str = Field(..., min_length=1, max_length=500)
    option_d: str = Field(..., min_length=1, max_length=500)
    correct_option: QuestionOption
    marks: int = Field(..., ge=1, le=10)
    explanation: Optional[str] = Field(None, max_length=1000)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM

    @validator('question_text')
    def validate_question_text(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Question text must be at least 10 characters long')
        return v.strip()

    @validator('option_a', 'option_b', 'option_c', 'option_d')
    def validate_options(cls, v):
        if len(v.strip()) < 1:
            raise ValueError('All options must have content')
        return v.strip()

class MockTestQuestionCreate(MockTestQuestionBase):
    pass

class MockTestQuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=10, max_length=1000)
    option_a: Optional[str] = Field(None, min_length=1, max_length=500)
    option_b: Optional[str] = Field(None, min_length=1, max_length=500)
    option_c: Optional[str] = Field(None, min_length=1, max_length=500)
    option_d: Optional[str] = Field(None, min_length=1, max_length=500)
    correct_option: Optional[QuestionOption] = None
    marks: Optional[int] = Field(None, ge=1, le=10)
    explanation: Optional[str] = Field(None, max_length=1000)
    difficulty: Optional[DifficultyLevel] = None

class MockTestQuestionResponse(MockTestQuestionBase):
    id: int
    mock_test_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MockTestBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    subject_id: int = Field(..., gt=0)
    time_limit_minutes: int = Field(60, ge=5, le=300)
    is_public: bool = False

    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Title must be at least 5 characters long')
        return v.strip()

class MockTestCreate(MockTestBase):
    questions: List[MockTestQuestionCreate] = Field(..., min_items=1)

    @validator('questions')
    def validate_questions(cls, v):
        if len(v) < 1:
            raise ValueError('Mock test must have at least one question')
        return v

class MockTestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    time_limit_minutes: Optional[int] = Field(None, ge=5, le=300)
    status: Optional[MockTestStatus] = None
    is_public: Optional[bool] = None

class MockTestResponse(MockTestBase):
    id: int
    instructor_id: int
    total_marks: int
    status: MockTestStatus
    created_at: datetime
    updated_at: Optional[datetime]
    questions: List[MockTestQuestionResponse] = []
    question_count: int = 0

    class Config:
        from_attributes = True

# Session schemas
class MockTestSessionCreate(BaseModel):
    mock_test_id: int = Field(..., gt=0)

class MockTestSessionResponse(BaseModel):
    id: int
    mock_test_id: int
    student_id: int
    status: MockTestSessionStatus
    started_at: Optional[datetime]
    submitted_at: Optional[datetime]
    total_score: float
    total_marks: int
    percentage: float
    time_taken_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True

# Answer schemas
class MockTestAnswerCreate(BaseModel):
    question_id: int = Field(..., gt=0)
    selected_option: Optional[QuestionOption] = None

class MockTestAnswerResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    selected_option: Optional[QuestionOption]
    is_correct: bool
    marks_obtained: float
    answered_at: datetime

    class Config:
        from_attributes = True

# Submission schemas
class MockTestSubmission(BaseModel):
    answers: List[MockTestAnswerCreate] = Field(..., min_items=1)

    @validator('answers')
    def validate_answers(cls, v):
        if len(v) < 1:
            raise ValueError('Must submit at least one answer')
        return v

# Results schemas
class MockTestResult(BaseModel):
    session_id: int
    total_score: float
    total_marks: int
    percentage: float
    correct_answers: int
    total_questions: int
    time_taken_minutes: int
    submitted_at: datetime
    answers: List[MockTestAnswerResponse] = []

class MockTestAnalyticsResponse(BaseModel):
    id: int
    session_id: int
    ai_analysis: Optional[Dict[str, Any]]
    strengths: Optional[List[str]]
    weaknesses: Optional[List[str]]
    recommendations: Optional[List[str]]
    performance_summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# AI Analysis schemas
class AIAnalysisRequest(BaseModel):
    session_id: int = Field(..., gt=0)

class AIAnalysisResponse(BaseModel):
    analysis: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    performance_summary: str

# List responses
class MockTestListResponse(BaseModel):
    tests: List[MockTestResponse]
    total: int
    page: int
    size: int

class MockTestSessionListResponse(BaseModel):
    sessions: List[MockTestSessionResponse]
    total: int
    page: int
    size: int
