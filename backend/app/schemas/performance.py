from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicPerformanceResponse(BaseModel):
    topic: str
    total_questions: int
    correct_answers: int
    accuracy: float
    average_time: Optional[float] = None
    last_attempt: Optional[datetime] = None

    class Config:
        from_attributes = True

class PerformanceResponse(BaseModel):
    user_id: int
    total_quizzes_taken: int
    average_score: float
    total_questions_answered: int
    total_correct_answers: int
    overall_accuracy: float
    topics_performance: List[TopicPerformanceResponse]
    weak_areas: List[str]
    strong_areas: List[str]

    class Config:
        from_attributes = True
