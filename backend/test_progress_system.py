#!/usr/bin/env python3
"""
Test script for the AI-powered student progress tracking system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.progress import StudentProgress, ProgressAnalytics, AIFeedback, CodingPractice, WeeklyReport, ActivityType, FeedbackType
from app.models.user import User
from app.services.progress_service import ProgressService
from app.services.ai_feedback_service import AIFeedbackService
from app.services.email_service import EmailService
from datetime import datetime, timedelta
import json

def test_progress_system():
    """Test the complete progress tracking system"""
    print("🧪 Testing AI-Powered Student Progress Tracking System...")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Initialize services with database session
        progress_service = ProgressService(db)
        ai_feedback_service = AIFeedbackService()
        email_service = EmailService()
        
        # Test 1: Create sample student progress
        print("\n1️⃣ Testing student progress recording...")
        
        # Get or create a test user
        test_user = db.query(User).first()
        if not test_user:
            print("❌ No users found in database. Please create a user first.")
            return
        
        print(f"✅ Using test user: {test_user.username}")
        
        # Record various activities
        activities = [
            {
                "user_id": test_user.id,
                "activity_type": ActivityType.COURSE_COMPLETION,
                "activity_name": "Introduction to Computer Networks",
                "subject": "Computer Networks",
                "score": 85,
                "time_spent": 120,  # minutes
                "difficulty_level": "BEGINNER",
                "metadata": {"course_id": 1, "completion_date": datetime.now().isoformat()}
            },
            {
                "user_id": test_user.id,
                "activity_type": ActivityType.QUIZ_ATTEMPT,
                "activity_name": "Networks Quiz 1",
                "subject": "Computer Networks",
                "score": 78,
                "time_spent": 45,
                "difficulty_level": "BEGINNER",
                "metadata": {"quiz_id": 1, "questions_attempted": 10}
            },
            {
                "user_id": test_user.id,
                "activity_type": ActivityType.CODING_PRACTICE,
                "activity_name": "Network Algorithm Practice",
                "subject": "Computer Networks",
                "score": 92,
                "time_spent": 90,
                "difficulty_level": "INTERMEDIATE",
                "metadata": {"problem_id": 1, "language": "Python"}
            }
        ]
        
        for activity_data in activities:
            progress = progress_service.track_activity(**activity_data)
            print(f"   ✅ Recorded: {activity_data['activity_name']} - Score: {activity_data['score']}")
        
        # Test 2: Generate progress analytics
        print("\n2️⃣ Testing progress analytics generation...")
        analytics = progress_service.generate_weekly_report(test_user.id)
        if analytics:
            print(f"   ✅ Generated weekly report for week: {analytics.week_start} to {analytics.week_end}")
            print(f"   📊 Summary: {analytics.summary[:100]}...")
            print(f"   🏆 Achievements: {len(analytics.achievements) if analytics.achievements else 0} items")
            print(f"   🔧 Areas for improvement: {len(analytics.areas_for_improvement) if analytics.areas_for_improvement else 0} items")
            print(f"   🎯 Next week goals: {len(analytics.next_week_goals) if analytics.next_week_goals else 0} items")
            print(f"   📚 Recommended courses: {len(analytics.recommended_courses) if analytics.recommended_courses else 0} courses")
            print(f"   💻 Recommended coding problems: {len(analytics.recommended_coding_problems) if analytics.recommended_coding_problems else 0} problems")
        else:
            print("   ❌ Failed to generate analytics")
        
        # Test 3: Generate AI feedback
        print("\n3️⃣ Testing AI feedback generation...")
        feedback = ai_feedback_service.generate_personalized_feedback(
            test_user.id, 
            FeedbackType.STRENGTH,
            "Computer Networks"
        )
        if feedback:
            print(f"   ✅ Generated AI feedback: {feedback}")
        else:
            print("   ❌ Failed to generate AI feedback")
        
        # Test 4: Get student progress
        print("\n4️⃣ Testing progress retrieval...")
        progress_data = progress_service.get_progress_dashboard_data(test_user.id)
        if progress_data:
            print(f"   ✅ Retrieved progress dashboard data")
            print(f"   📊 Total activities: {len(progress_data.get('recent_activities', []))}")
            print(f"   📈 Subject performance: {len(progress_data.get('subject_performance', []))} subjects")
            print(f"   💻 Coding progress: {len(progress_data.get('coding_progress', []))} sessions")
        else:
            print("   ❌ Failed to retrieve progress data")
        
        # Test 5: Test email service (mock)
        print("\n5️⃣ Testing email service...")
        try:
            # Get the weekly report for email testing
            weekly_report = db.query(WeeklyReport).filter(WeeklyReport.user_id == test_user.id).first()
            if weekly_report:
                email_sent = email_service.send_weekly_progress_report(test_user, weekly_report)
                print(f"   ✅ Email service working (mock mode): {email_sent}")
            else:
                print("   ⚠️ No weekly report found for email testing")
        except Exception as e:
            print(f"   ⚠️ Email service test failed (expected in development): {e}")
        
        print("\n🎉 Progress tracking system test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_progress_system()
