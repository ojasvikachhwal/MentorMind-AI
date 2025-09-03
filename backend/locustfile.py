"""
Performance testing with Locust for the MentorMind API
"""
from locust import HttpUser, task, between
import json
import random

class MentorMindUser(HttpUser):
    """Simulate a user interacting with the MentorMind platform."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Login and get authentication token."""
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        response = self.client.post("/api/v1/auth/login", data=login_data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(3)
    def view_dashboard(self):
        """View progress dashboard (high frequency)."""
        if self.token:
            self.client.get("/api/v1/progress/dashboard", headers=self.headers)
    
    @task(2)
    def get_course_recommendations(self):
        """Get course recommendations."""
        if self.token:
            self.client.get("/api/v1/courses/recommendations", headers=self.headers)
    
    @task(1)
    def submit_assessment(self):
        """Submit an assessment."""
        if self.token:
            assessment_data = {
                "subject": random.choice(["Computer Science", "Mathematics", "Physics"]),
                "answers": [
                    {"question_id": i, "selected_answer": random.choice(["A", "B", "C", "D"])}
                    for i in range(1, 11)
                ],
                "time_taken": random.randint(1800, 3600)
            }
            
            self.client.post(
                "/api/v1/assessment/submit",
                json=assessment_data,
                headers=self.headers
            )
    
    @task(1)
    def track_progress(self):
        """Track learning progress."""
        if self.token:
            progress_data = {
                "activity_type": random.choice(["COURSE_COMPLETION", "QUIZ_ATTEMPT", "CODING_PRACTICE"]),
                "activity_name": f"Test Activity {random.randint(1, 100)}",
                "subject": random.choice(["Computer Science", "Mathematics", "Physics"]),
                "score": random.uniform(60.0, 100.0),
                "time_spent": random.randint(30, 180),
                "difficulty_level": random.choice(["BEGINNER", "INTERMEDIATE", "ADVANCED"]),
                "metadata": {"course_id": random.randint(1, 50)}
            }
            
            self.client.post(
                "/api/v1/progress/update",
                json=progress_data,
                headers=self.headers
            )
    
    @task(1)
    def get_ai_feedback(self):
        """Get AI-generated feedback."""
        if self.token:
            feedback_data = {
                "feedback_type": random.choice(["STRENGTH", "WEAKNESS", "IMPROVEMENT"]),
                "subject": random.choice(["Computer Science", "Mathematics", "Physics"])
            }
            
            self.client.post(
                "/api/v1/ai/feedback",
                json=feedback_data,
                headers=self.headers
            )
    
    @task(1)
    def submit_coding_practice(self):
        """Submit coding practice solution."""
        if self.token:
            coding_data = {
                "problem_title": f"Problem {random.randint(1, 100)}",
                "language": random.choice(["Python", "JavaScript", "Java"]),
                "solution_code": "def solution():\n    return True",
                "problem_difficulty": random.choice(["EASY", "MEDIUM", "HARD"])
            }
            
            self.client.post(
                "/api/v1/coding/practice",
                json=coding_data,
                headers=self.headers
            )

class AdminUser(HttpUser):
    """Simulate admin user operations."""
    
    wait_time = between(2, 5)
    weight = 1  # Lower weight for admin users
    
    def on_start(self):
        """Admin login."""
        login_data = {
            "username": "admin",
            "password": "adminpass123"
        }
        
        response = self.client.post("/api/v1/admin/login", json=login_data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(2)
    def view_admin_dashboard(self):
        """View admin dashboard."""
        if self.token:
            self.client.get("/api/v1/admin/dashboard", headers=self.headers)
    
    @task(1)
    def view_student_reports(self):
        """View student reports."""
        if self.token:
            self.client.get("/api/v1/admin/reports/students", headers=self.headers)
    
    @task(1)
    def view_course_analytics(self):
        """View course analytics."""
        if self.token:
            self.client.get("/api/v1/admin/reports/courses", headers=self.headers)
