#!/usr/bin/env python3
"""
Test script for the new course recommendation endpoint.
This script tests the /courses/recommendations/{student_id} endpoint.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "teststudent"
TEST_PASSWORD = "password"

def test_course_recommendations():
    """Test the course recommendations endpoint."""
    print("🧪 Testing Course Recommendations Endpoint")
    print("=" * 50)
    
    # Step 1: Login to get access token
    print("\n1. Logging in to get access token...")
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("✅ Login successful!")
            print(f"   - Access token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed with status {response.status_code}")
            print(f"   - Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Set up headers for authenticated requests
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test getting recommendations for the current user
    print("\n2. Testing recommendations for current user...")
    try:
        response = requests.get(
            f"{BASE_URL}/courses/recommendations/me",
            headers=headers,
            params={"num_recommendations": 3}
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ Current user recommendations retrieved!")
            print(f"   - Student ID: {recommendations.get('student_id')}")
            print(f"   - Student Name: {recommendations.get('student_name')}")
            print(f"   - Number of subjects: {len(recommendations.get('recommendations', []))}")
            
            # Display recommendations
            for i, rec in enumerate(recommendations.get('recommendations', []), 1):
                print(f"\n   Subject {i}: {rec.get('subject')}")
                print(f"   - Weakness: {rec.get('weakness')}")
                print(f"   - Performance Level: {rec.get('performance_level')}")
                print(f"   - Score: {rec.get('percent_correct')}%")
                print(f"   - Recommended Courses: {len(rec.get('recommended_courses', []))}")
                
                for j, course in enumerate(rec.get('recommended_courses', [])[:2], 1):
                    print(f"     {j}. {course.get('title')} ({course.get('level')})")
        else:
            print(f"❌ Failed to get current user recommendations: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting current user recommendations: {e}")
    
    # Step 3: Test getting recommendations for a specific student ID
    print("\n3. Testing recommendations for specific student ID...")
    try:
        # First, get the user ID from the previous response
        if 'recommendations' in locals():
            student_id = recommendations.get('student_id')
            if student_id:
                response = requests.get(
                    f"{BASE_URL}/courses/recommendations/{student_id}",
                    headers=headers,
                    params={"num_recommendations": 5}
                )
                
                if response.status_code == 200:
                    specific_recommendations = response.json()
                    print("✅ Specific student recommendations retrieved!")
                    print(f"   - Student ID: {specific_recommendations.get('student_id')}")
                    print(f"   - Student Name: {specific_recommendations.get('student_name')}")
                    print(f"   - Number of subjects: {len(specific_recommendations.get('recommendations', []))}")
                else:
                    print(f"❌ Failed to get specific student recommendations: {response.status_code}")
                    print(f"   - Response: {response.text}")
            else:
                print("⚠️  No student ID available for testing specific student endpoint")
        else:
            print("⚠️  No recommendations available for testing specific student endpoint")
    except Exception as e:
        print(f"❌ Error getting specific student recommendations: {e}")
    
    # Step 4: Test ML recommendations endpoint
    print("\n4. Testing ML recommendations endpoint...")
    try:
        if 'student_id' in locals():
            response = requests.get(
                f"{BASE_URL}/courses/recommendations/ml/{student_id}",
                headers=headers,
                params={"num_recommendations": 3}
            )
            
            if response.status_code == 200:
                ml_recommendations = response.json()
                print("✅ ML recommendations retrieved!")
                print(f"   - Student ID: {ml_recommendations.get('student_id')}")
                print(f"   - Student Name: {ml_recommendations.get('student_name')}")
                print(f"   - Number of subjects: {len(ml_recommendations.get('recommendations', []))}")
            else:
                print(f"❌ Failed to get ML recommendations: {response.status_code}")
                print(f"   - Response: {response.text}")
        else:
            print("⚠️  No student ID available for testing ML recommendations endpoint")
    except Exception as e:
        print(f"❌ Error getting ML recommendations: {e}")
    
    # Step 5: Test error handling
    print("\n5. Testing error handling...")
    try:
        # Test with invalid student ID
        response = requests.get(
            f"{BASE_URL}/courses/recommendations/99999",
            headers=headers
        )
        
        if response.status_code == 404:
            print("✅ Error handling working correctly for invalid student ID")
        else:
            print(f"⚠️  Unexpected response for invalid student ID: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing error handling: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Course Recommendations Testing Complete!")
    return True

def main():
    """Main test function."""
    print("🚀 Starting Course Recommendations API Tests")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Make sure you have test data in the database")
    
    try:
        success = test_course_recommendations()
        if success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed!")
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()
