"""
Pydantic schemas for progress tracking and AI feedback.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ActivityTypeEnum(str, Enum):
    COURSE_COMPLETION = "course_completion"
    QUIZ_ATTEMPT = "quiz_attempt"
    CODING_PRACTICE = "coding_practice"
    ASSESSMENT = "assessment"
    STUDY_TIME = "study_time"

class FeedbackTypeEnum(str, Enum):
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    RECOMMENDATION = "recommendation"
    ENCOURAGEMENT = "encouragement"
    WARNING = "warning"

# Progress Activity Schemas
class ProgressActivityCreate(BaseModel):
    activity_type: ActivityTypeEnum
    activity_name: str = Field(..., min_length=1, max_length=200)
    subject: Optional[str] = Field(None, max_length=100)
    score: Optional[float] = Field(None, ge=0, le=100)
    time_spent: int = Field(0, ge=0)
    difficulty_level: Optional[str] = Field(None, max_length=20)
    activity_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class ProgressActivityResponse(BaseModel):
    id: int
    user_id: int
    activity_type: ActivityTypeEnum
    activity_name: str
    subject: Optional[str]
    score: Optional[float]
    time_spent: int
    difficulty_level: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Coding Practice Schemas
class CodingPracticeCreate(BaseModel):
    problem_title: str = Field(..., min_length=1, max_length=200)
    problem_difficulty: str = Field(..., max_length=20)
    language: str = Field(..., max_length=50)
    solution_code: str = Field(..., min_length=1)
    test_cases_passed: int = Field(..., ge=0)
    total_test_cases: int = Field(..., ge=1)
    execution_time: Optional[float] = Field(None, ge=0)
    memory_usage: Optional[float] = Field(None, ge=0)
    time_spent: int = Field(0, ge=0)

class CodingPracticeResponse(BaseModel):
    id: int
    user_id: int
    problem_title: str
    problem_difficulty: str
    language: str
    test_cases_passed: int
    total_test_cases: int
    execution_time: Optional[float]
    memory_usage: Optional[float]
    ai_feedback: Optional[str]
    optimization_suggestions: Optional[List[str]]
    score: Optional[float]
    time_spent: int
    created_at: datetime

    class Config:
        from_attributes = True

# Weekly Analytics Schemas
class WeeklyAnalyticsResponse(BaseModel):
    id: int
    user_id: int
    week_start: datetime
    week_end: datetime
    total_study_time: int
    courses_completed: int
    quizzes_taken: int
    coding_sessions: int
    average_quiz_score: float
    average_coding_score: float
    subject_performance: Optional[Dict[str, Any]]
    strengths: Optional[List[str]]
    weaknesses: Optional[List[str]]
    recommendations: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True

# Weekly Report Schemas
class WeeklyReportResponse(BaseModel):
    id: int
    user_id: int
    week_start: datetime
    week_end: datetime
    summary: str
    achievements: Optional[List[str]]
    areas_for_improvement: Optional[List[str]]
    next_week_goals: Optional[List[str]]
    recommended_courses: Optional[List[Dict[str, Any]]]
    recommended_coding_problems: Optional[List[Dict[str, Any]]]
    email_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True

# AI Feedback Schemas
class AIFeedbackResponse(BaseModel):
    id: int
    user_id: int
    feedback_type: FeedbackTypeEnum
    subject: Optional[str]
    title: str
    message: str
    confidence_score: float
    is_read: bool
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Dashboard Data Schemas
class DailyActivityData(BaseModel):
    date: str
    study_time: int
    activities: int
    quiz_score: float
    coding_score: float

class SubjectPerformanceData(BaseModel):
    subject: str
    activities: int
    total_time: int
    scores: List[float]
    average_score: float

class CodingProgressData(BaseModel):
    date: str
    problem: str
    difficulty: str
    language: str
    score: Optional[float]
    execution_time: Optional[float]
    test_cases_passed: int
    total_test_cases: int

class WeeklyAnalyticsData(BaseModel):
    week_start: str
    total_study_time: int
    courses_completed: int
    quizzes_taken: int
    coding_sessions: int
    average_quiz_score: float
    average_coding_score: float

class RecentFeedbackData(BaseModel):
    id: int
    type: FeedbackTypeEnum
    title: str
    message: str
    subject: Optional[str]
    created_at: str
    is_read: bool

class ProgressSummary(BaseModel):
    total_activities: int
    total_coding_sessions: int
    total_study_time: int
    average_quiz_score: float
    average_coding_score: float

class ProgressDashboardResponse(BaseModel):
    daily_activity: List[DailyActivityData]
    subject_performance: List[SubjectPerformanceData]
    coding_progress: List[CodingProgressData]
    recent_feedback: List[RecentFeedbackData]
    weekly_analytics: List[WeeklyAnalyticsData]
    summary: ProgressSummary

# Learning Pattern Analysis Schemas
class LearningPatternInsights(BaseModel):
    insights: List[str]
    peak_hours: List[int]
    subject_distribution: Dict[str, int]
    difficulty_progression: List[Dict[str, Any]]

# Course Recommendation Schemas
class CourseRecommendation(BaseModel):
    id: int
    title: str
    level: str
    subject: Optional[str]
    url: Optional[str]

class CodingProblemRecommendation(BaseModel):
    title: str
    difficulty: str
    topic: str
    url: str

# Email Report Schemas
class EmailReportData(BaseModel):
    user_name: str
    week_start: str
    week_end: str
    summary: str
    achievements: List[str]
    areas_for_improvement: List[str]
    next_week_goals: List[str]
    recommended_courses: List[CourseRecommendation]
    recommended_coding_problems: List[CodingProblemRecommendation]

# Progress Statistics Schemas
class ProgressStatistics(BaseModel):
    total_study_hours: float
    total_activities: int
    courses_completed: int
    quizzes_taken: int
    coding_sessions: int
    average_quiz_score: float
    average_coding_score: float
    current_streak: int
    longest_streak: int
    favorite_subject: Optional[str]
    improvement_rate: float

# Goal Setting Schemas
class LearningGoal(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    subject: Optional[str] = None
    difficulty_level: Optional[str] = None
    is_completed: bool = False
    created_at: Optional[datetime] = None

class GoalProgress(BaseModel):
    goal_id: int
    progress_percentage: float = Field(..., ge=0, le=100)
    notes: Optional[str] = None
    updated_at: datetime
