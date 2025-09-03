"""
Pydantic schemas for question analysis.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuestionAnalysisRequest(BaseModel):
    """Request schema for question analysis."""
    subject: str = Field(..., description="Subject of the question (e.g., 'Mathematics', 'Physics')")
    text: str = Field(..., description="Question text to analyze", min_length=1, max_length=2000)
    use_ml: Optional[bool] = Field(default=False, description="Whether to use ML model if available")

class QuestionAnalysisResponse(BaseModel):
    """Response schema for question analysis."""
    question: str = Field(..., description="Original question text")
    subject: str = Field(..., description="Subject of the question")
    difficulty: str = Field(..., description="Classified difficulty level (easy/medium/hard)")
    tags: List[str] = Field(..., description="Extracted tags from the question")
    confidence: float = Field(..., description="Confidence score for the analysis", ge=0.0, le=1.0)
    analysis_method: str = Field(..., description="Method used for analysis (rule_based/ml_model)")
    word_count: int = Field(..., description="Number of words in the question")
    complexity_score: float = Field(..., description="Overall complexity score", ge=0.0, le=1.0)
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")

class BatchQuestionAnalysisRequest(BaseModel):
    """Request schema for batch question analysis."""
    questions: List[QuestionAnalysisRequest] = Field(..., description="List of questions to analyze")
    use_ml: Optional[bool] = Field(default=False, description="Whether to use ML model if available")

class BatchQuestionAnalysisResponse(BaseModel):
    """Response schema for batch question analysis."""
    results: List[QuestionAnalysisResponse] = Field(..., description="Analysis results for each question")
    total_questions: int = Field(..., description="Total number of questions processed")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")
    analysis_method: str = Field(..., description="Method used for analysis")

class QuestionAnalysisStats(BaseModel):
    """Schema for question analysis statistics."""
    total_questions_analyzed: int = Field(..., description="Total number of questions analyzed")
    difficulty_distribution: dict = Field(..., description="Distribution of difficulty levels")
    tag_frequency: dict = Field(..., description="Frequency of extracted tags")
    average_confidence: float = Field(..., description="Average confidence score")
    average_complexity: float = Field(..., description="Average complexity score")
    analysis_methods_used: dict = Field(..., description="Methods used for analysis")

class QuestionUploadRequest(BaseModel):
    """Request schema for uploading questions with automatic analysis."""
    subject: str = Field(..., description="Subject of the questions")
    questions: List[str] = Field(..., description="List of question texts")
    auto_analyze: Optional[bool] = Field(default=True, description="Whether to automatically analyze questions")
    save_to_db: Optional[bool] = Field(default=True, description="Whether to save questions to database")

class QuestionUploadResponse(BaseModel):
    """Response schema for question upload."""
    total_questions: int = Field(..., description="Total number of questions uploaded")
    analyzed_questions: int = Field(..., description="Number of questions analyzed")
    saved_questions: int = Field(..., description="Number of questions saved to database")
    analysis_results: List[QuestionAnalysisResponse] = Field(..., description="Analysis results for uploaded questions")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")

class QuestionSearchRequest(BaseModel):
    """Request schema for searching questions by tags and difficulty."""
    tags: Optional[List[str]] = Field(None, description="Tags to search for")
    difficulty: Optional[str] = Field(None, description="Difficulty level to filter by")
    subject: Optional[str] = Field(None, description="Subject to filter by")
    min_complexity: Optional[float] = Field(None, description="Minimum complexity score", ge=0.0, le=1.0)
    max_complexity: Optional[float] = Field(None, description="Maximum complexity score", ge=0.0, le=1.0)
    limit: Optional[int] = Field(default=50, description="Maximum number of results to return", le=100)

class QuestionSearchResponse(BaseModel):
    """Response schema for question search."""
    questions: List[QuestionAnalysisResponse] = Field(..., description="Matching questions")
    total_found: int = Field(..., description="Total number of matching questions")
    search_criteria: dict = Field(..., description="Search criteria used")
    search_time_ms: float = Field(..., description="Search execution time in milliseconds")
