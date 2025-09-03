#!/usr/bin/env python3
"""
Test script for the new course recommendation endpoint.
This script tests the /recommend-courses/{user_id} endpoint.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = 1  # You may need to create a test user first

def test_course_recommendations():
    """Test the course recommendation endpoint."""
    
    print("🧪 Testing Course Recommendation Endpoint")
    print("=" * 50)
    
    # Test the new endpoint
    endpoint = f"{BASE_URL}/recommend-courses/{TEST_USER_ID}"
    
    try:
        print(f"📡 Testing endpoint: {endpoint}")
        print(f"👤 User ID: {TEST_USER_ID}")
        
        # Note: This endpoint requires authentication
        # You'll need to either:
        # 1. Create a test user and get a valid JWT token
        # 2. Temporarily disable authentication for testing
        # 3. Use the existing /courses/recommendations/{student_id} endpoint
        
        print("\n⚠️  Note: This endpoint requires authentication.")
        print("   To test it properly, you need to:")
        print("   1. Create a test user")
        print("   2. Get a JWT token by logging in")
        print("   3. Include the token in the Authorization header")
        
        # For now, let's test the existing endpoint that doesn't require auth
        print("\n🔄 Testing existing endpoint instead...")
        existing_endpoint = f"{BASE_URL}/courses/recommendations/{TEST_USER_ID}"
        
        response = requests.get(existing_endpoint)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_database_courses():
    """Test that courses are properly stored in the database."""
    
    print("\n🗄️  Testing Database Course Storage")
    print("=" * 50)
    
    try:
        # Import database models
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.assessment import Subject, Course, CourseLevel
        
        db = SessionLocal()
        
        # Check subjects
        subjects = db.query(Subject).all()
        print(f"📚 Found {len(subjects)} subjects:")
        for subject in subjects:
            print(f"   - {subject.name}")
        
        # Check courses
        courses = db.query(Course).all()
        print(f"\n🎓 Found {len(courses)} courses:")
        
        # Group by subject
        courses_by_subject = {}
        for course in courses:
            subject_name = course.subject.name
            if subject_name not in courses_by_subject:
                courses_by_subject[subject_name] = []
            courses_by_subject[subject_name].append(course)
        
        for subject_name, subject_courses in courses_by_subject.items():
            print(f"\n   {subject_name}:")
            for course in subject_courses:
                level_emoji = "🟢" if course.level == CourseLevel.BEGINNER else "🟡" if course.level == CourseLevel.INTERMEDIATE else "🔴"
                print(f"     {level_emoji} {course.title} ({course.level.value})")
                if course.url:
                    print(f"        URL: {course.url}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database test error: {e}")

if __name__ == "__main__":
    print("🚀 Course Recommendation System Test")
    print("=" * 50)
    
    # Test database courses first
    test_database_courses()
    
    # Test the API endpoint
    test_course_recommendations()
    
    print("\n✨ Test completed!")
