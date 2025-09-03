"""
Test API endpoints for authentication, assessment, recommendations, and progress tracking
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_user_registration(client: TestClient, db_session: Session):
    """Test user registration endpoint."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123",
        "full_name": "New User"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_user_login(client: TestClient, test_user):
    """Test user login endpoint."""
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data

def test_progress_tracking(client: TestClient, test_user, db_session: Session):
    """Test progress tracking endpoint."""
    # First login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Track activity
    progress_data = {
        "activity_type": "COURSE_COMPLETION",
        "activity_name": "Test Course",
        "subject": "Computer Science",
        "score": 85.0,
        "time_spent": 120,
        "difficulty_level": "INTERMEDIATE",
        "metadata": {"course_id": 1}
    }
    
    response = client.post(
        "/api/v1/progress/update",
        json=progress_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["activity_name"] == progress_data["activity_name"]
    assert data["score"] == progress_data["score"]

def test_progress_report(client: TestClient, test_user, test_progress_data, db_session: Session):
    """Test progress report generation endpoint."""
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Get progress report
    response = client.get(
        f"/api/v1/progress/report/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "achievements" in data

def test_course_recommendations(client: TestClient, test_user, db_session: Session):
    """Test course recommendations endpoint."""
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Get recommendations
    response = client.get(
        "/api/v1/courses/recommendations",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_assessment_submission(client: TestClient, test_user, db_session: Session):
    """Test assessment submission endpoint."""
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Submit assessment
    assessment_data = {
        "subject": "Computer Science",
        "answers": [
            {"question_id": 1, "selected_answer": "A"},
            {"question_id": 2, "selected_answer": "B"}
        ],
        "time_taken": 1800
    }
    
    response = client.post(
        "/api/v1/assessment/submit",
        json=assessment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "recommendations" in data

def test_ai_feedback(client: TestClient, test_user, db_session: Session):
    """Test AI feedback generation endpoint."""
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Get AI feedback
    feedback_data = {
        "feedback_type": "STRENGTH",
        "subject": "Computer Science"
    }
    
    response = client.post(
        "/api/v1/ai/feedback",
        json=feedback_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "confidence_score" in data

def test_coding_practice(client: TestClient, test_user, db_session: Session):
    """Test coding practice submission endpoint."""
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Submit coding solution
    coding_data = {
        "problem_title": "Two Sum",
        "language": "Python",
        "solution_code": "def two_sum(nums, target):\n    return [0, 1]",
        "problem_difficulty": "EASY"
    }
    
    response = client.post(
        "/api/v1/coding/practice",
        json=coding_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "ai_feedback" in data
