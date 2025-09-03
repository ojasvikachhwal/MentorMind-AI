from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuestionCreate(BaseModel):
    text: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None
    difficulty: str = "medium"
    topic: str

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    options: List[str]
    explanation: Optional[str] = None
    difficulty_score: float
    question_type: str

    class Config:
        from_attributes = True

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    topic: str
    difficulty: str = "medium"
    time_limit: Optional[int] = None  # in minutes

class QuizResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    topic: str
    difficulty_level: str
    time_limit: Optional[int] = None
    question_count: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class QuizAttemptCreate(BaseModel):
    quiz_id: int
    answers: List[int]  # List of selected option indices

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: float
    total_questions: int
    correct_answers: int
    time_taken: Optional[int] = None  # in seconds
    completed_at: datetime

    class Config:
        from_attributes = True
