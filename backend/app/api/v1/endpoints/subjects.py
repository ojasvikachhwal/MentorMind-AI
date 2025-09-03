from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Any

from app.core.database import get_db
from app.schemas.assessment import SubjectResponse
from app.services.assessment_service import AssessmentService

router = APIRouter()

@router.get("/subjects", response_model=List[SubjectResponse])
async def get_subjects(db: Session = Depends(get_db)) -> Any:
    """
    Get all available subjects for assessment.
    """
    subjects = AssessmentService.get_subjects(db)
    return subjects
