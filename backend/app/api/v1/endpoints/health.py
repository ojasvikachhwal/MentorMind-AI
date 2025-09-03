from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
import redis
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "mentormind-backend",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check including database and Redis connectivity.
    """
    health_status = {
        "status": "healthy",
        "service": "mentormind-backend",
        "version": "1.0.0",
        "checks": {
            "database": "unknown",
            "redis": "unknown"
        }
    }
    
    # Check database connectivity
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Redis connectivity
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    return health_status

@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/container orchestration.
    """
    return {
        "status": "ready",
        "service": "mentormind-backend"
    }

@router.get("/health/live")
async def liveness_check():
    """
    Liveness check for Kubernetes/container orchestration.
    """
    return {
        "status": "alive",
        "service": "mentormind-backend"
    }
