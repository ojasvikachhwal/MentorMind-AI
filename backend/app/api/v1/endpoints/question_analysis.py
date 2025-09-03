"""
FastAPI endpoints for question analysis and NLP processing.
"""

import time
from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.nlp_analysis import QuestionAnalyzer
from app.schemas.question_analysis import (
    QuestionAnalysisRequest, QuestionAnalysisResponse,
    BatchQuestionAnalysisRequest, BatchQuestionAnalysisResponse,
    QuestionAnalysisStats, QuestionUploadRequest, QuestionUploadResponse,
    QuestionSearchRequest, QuestionSearchResponse
)

router = APIRouter()

# Initialize the question analyzer
question_analyzer = QuestionAnalyzer()

@router.post("/questions/analyze", response_model=QuestionAnalysisResponse)
async def analyze_question(
    request: QuestionAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Analyze a single question to determine difficulty and extract tags.
    
    This endpoint uses NLP analysis to:
    - Classify question difficulty (easy/medium/hard)
    - Extract relevant tags using spaCy and NLTK
    - Calculate complexity scores
    - Provide confidence metrics
    
    Args:
        request: Question analysis request with subject and text
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        QuestionAnalysisResponse with analysis results
    """
    start_time = time.time()
    
    try:
        # Analyze the question
        analysis = question_analyzer.analyze_question(
            question_text=request.text,
            subject=request.subject
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Create response
        response = QuestionAnalysisResponse(
            question=request.text,
            subject=request.subject,
            difficulty=analysis.difficulty,
            tags=analysis.tags,
            confidence=analysis.confidence,
            analysis_method=analysis.analysis_method,
            word_count=analysis.word_count,
            complexity_score=analysis.complexity_score,
            processing_time_ms=processing_time
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing question: {str(e)}"
        )

@router.post("/questions/analyze/batch", response_model=BatchQuestionAnalysisResponse)
async def analyze_questions_batch(
    request: BatchQuestionAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Analyze multiple questions in batch for efficiency.
    
    Args:
        request: Batch question analysis request
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        BatchQuestionAnalysisResponse with results for all questions
    """
    start_time = time.time()
    
    try:
        # Prepare questions for batch analysis
        questions_data = [
            {"text": q.text, "subject": q.subject}
            for q in request.questions
        ]
        
        # Perform batch analysis
        analyses = question_analyzer.batch_analyze(questions_data)
        
        # Convert to response format
        results = []
        for i, analysis in enumerate(analyses):
            result = QuestionAnalysisResponse(
                question=request.questions[i].text,
                subject=request.questions[i].subject,
                difficulty=analysis.difficulty,
                tags=analysis.tags,
                confidence=analysis.confidence,
                analysis_method=analysis.analysis_method,
                word_count=analysis.word_count,
                complexity_score=analysis.complexity_score
            )
            results.append(result)
        
        # Calculate total processing time
        total_time = (time.time() - start_time) * 1000
        
        return BatchQuestionAnalysisResponse(
            results=results,
            total_questions=len(results),
            processing_time_ms=total_time,
            analysis_method=question_analyzer.get_analysis_stats()["analysis_method"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch analysis: {str(e)}"
        )

@router.post("/questions/upload", response_model=QuestionUploadResponse)
async def upload_questions_with_analysis(
    request: QuestionUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Upload multiple questions with automatic analysis and optional database storage.
    
    This endpoint is useful for admins/teachers to bulk upload questions
    and get automatic difficulty classification and tagging.
    
    Args:
        request: Question upload request
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        QuestionUploadResponse with upload and analysis results
    """
    start_time = time.time()
    
    try:
        # Check if user has permission to upload questions
        if current_user.role.value not in ["admin", "teacher"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins and teachers can upload questions"
            )
        
        total_questions = len(request.questions)
        analyzed_questions = 0
        saved_questions = 0
        analysis_results = []
        
        if request.auto_analyze:
            # Analyze all questions
            questions_data = [
                {"text": q, "subject": request.subject}
                for q in request.questions
            ]
            
            analyses = question_analyzer.batch_analyze(questions_data)
            analyzed_questions = len(analyses)
            
            # Convert to response format
            for i, analysis in enumerate(analyses):
                result = QuestionAnalysisResponse(
                    question=request.questions[i],
                    subject=request.subject,
                    difficulty=analysis.difficulty,
                    tags=analysis.tags,
                    confidence=analysis.confidence,
                    analysis_method=analysis.analysis_method,
                    word_count=analysis.word_count,
                    complexity_score=analysis.complexity_score
                )
                analysis_results.append(result)
        
        # TODO: Implement database storage if save_to_db is True
        # This would involve saving to the questions table with difficulty and tags
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        return QuestionUploadResponse(
            total_questions=total_questions,
            analyzed_questions=analyzed_questions,
            saved_questions=saved_questions,
            analysis_results=analysis_results,
            processing_time_ms=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading questions: {str(e)}"
        )

@router.get("/questions/search", response_model=QuestionSearchResponse)
async def search_questions(
    tags: Optional[List[str]] = Query(None, description="Tags to search for"),
    difficulty: Optional[str] = Query(None, description="Difficulty level (easy/medium/hard)"),
    subject: Optional[str] = Query(None, description="Subject to filter by"),
    min_complexity: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum complexity score"),
    max_complexity: Optional[float] = Query(None, ge=0.0, le=1.0, description="Maximum complexity score"),
    limit: int = Query(default=50, le=100, description="Maximum number of results"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Search for questions based on tags, difficulty, and complexity criteria.
    
    Args:
        tags: List of tags to search for
        difficulty: Difficulty level filter
        subject: Subject filter
        min_complexity: Minimum complexity score
        max_complexity: Maximum complexity score
        limit: Maximum number of results
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        QuestionSearchResponse with matching questions
    """
    start_time = time.time()
    
    try:
        # TODO: Implement actual database search
        # This would query the questions table with the specified filters
        
        # For now, return empty results
        search_criteria = {
            "tags": tags,
            "difficulty": difficulty,
            "subject": subject,
            "min_complexity": min_complexity,
            "max_complexity": max_complexity,
            "limit": limit
        }
        
        search_time = (time.time() - start_time) * 1000
        
        return QuestionSearchResponse(
            questions=[],
            total_found=0,
            search_criteria=search_criteria,
            search_time_ms=search_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching questions: {str(e)}"
        )

@router.get("/questions/analysis/stats", response_model=QuestionAnalysisStats)
async def get_analysis_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get statistics about question analysis.
    
    Args:
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        QuestionAnalysisStats with analysis statistics
    """
    try:
        # TODO: Implement actual statistics calculation from database
        # This would aggregate data from the questions table
        
        # For now, return sample statistics
        stats = QuestionAnalysisStats(
            total_questions_analyzed=0,
            difficulty_distribution={"easy": 0, "medium": 0, "hard": 0},
            tag_frequency={},
            average_confidence=0.0,
            average_complexity=0.0,
            analysis_methods_used={"rule_based": 0, "ml_model": 0}
        )
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting analysis statistics: {str(e)}"
        )

@router.get("/questions/analysis/analyzer-info")
async def get_analyzer_information(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get information about the question analyzer configuration and status.
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        Dictionary with analyzer information
    """
    try:
        analyzer_stats = question_analyzer.get_analysis_stats()
        return {
            "message": "Question Analyzer Information",
            "analyzer_status": "active",
            "configuration": analyzer_stats,
            "capabilities": [
                "Difficulty classification (easy/medium/hard)",
                "Tag extraction using NLP",
                "Complexity scoring",
                "Batch processing",
                "ML model ready (future enhancement)"
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting analyzer information: {str(e)}"
        )

@router.post("/questions/analysis/update-model")
async def update_ml_model(
    model_info: dict,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update the ML model used for question analysis.
    
    This endpoint allows admins to update the underlying ML model
    (e.g., Hugging Face model) without restarting the service.
    
    Args:
        model_info: Information about the new model
        current_user: Currently authenticated user
        
    Returns:
        Success message
    """
    try:
        # Check if user has admin privileges
        if current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update ML models"
            )
        
        # TODO: Implement actual model loading and updating
        # This would load the new model and update the analyzer
        
        return {
            "message": "ML model update initiated",
            "model_info": model_info,
            "status": "pending"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating ML model: {str(e)}"
        )
