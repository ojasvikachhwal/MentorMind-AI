#!/usr/bin/env python3
"""
Simple test script to verify the assessment system functionality.
"""

import sys
import os
import requests
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_assessment_system():
    """Test the assessment system endpoints."""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 Testing Assessment System...")
    print("=" * 50)
    
    # Test 1: Get subjects
    print("\n1. Testing GET /subjects...")
    try:
        response = requests.get(f"{base_url}/assessment/subjects")
        if response.status_code == 200:
            subjects = response.json()
            print(f"✅ Success! Found {len(subjects)} subjects")
            for subject in subjects[:3]:  # Show first 3
                print(f"   - {subject['name']}")
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Register a test user
    print("\n2. Testing user registration...")
    try:
        register_data = {
            "username": "teststudent",
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test Student"
        }
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        if response.status_code == 200:
            print("✅ User registered successfully")
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Login to get token
    print("\n3. Testing user login...")
    try:
        login_data = {
            "username": "teststudent",
            "password": "password123"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("✅ Login successful")
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Start assessment
    print("\n4. Testing assessment start...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        assessment_data = {
            "subject_ids": [1, 2],  # Test with first 2 subjects
            "num_questions_per_subject": 5
        }
        response = requests.post(
            f"{base_url}/assessment/assessment/start", 
            json=assessment_data,
            headers=headers
        )
        if response.status_code == 200:
            assessment_response = response.json()
            session_id = assessment_response["session_id"]
            questions = assessment_response["questions"]
            print(f"✅ Assessment started! Session ID: {session_id}")
            print(f"   - Questions received: {len(questions)}")
        else:
            print(f"❌ Assessment start failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Submit assessment answers
    print("\n5. Testing assessment submission...")
    try:
        # Create sample answers (all correct for testing)
        answers = []
        for question in questions:
            answers.append({
                "question_id": question["id"],
                "selected_index": 0  # Assume first option is correct for testing
            })
        
        submit_data = {"answers": answers}
        response = requests.post(
            f"{base_url}/assessment/assessment/{session_id}/submit",
            json=submit_data,
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Assessment submitted successfully!")
            print(f"   - Results for {len(result['results'])} subjects")
            for subject_result in result['results']:
                print(f"   - {subject_result['subject_name']}: {subject_result['percent_correct']}% ({subject_result['level']})")
        else:
            print(f"❌ Assessment submission failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 6: Get latest recommendations
    print("\n6. Testing latest recommendations...")
    try:
        response = requests.get(
            f"{base_url}/assessment/recommendations/latest",
            headers=headers
        )
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ Latest recommendations retrieved!")
            print(f"   - Session ID: {recommendations['session_id']}")
            print(f"   - Results for {len(recommendations['results'])} subjects")
        else:
            print(f"❌ Recommendations failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All assessment tests passed!")
    return True

def main():
    """Main function to run tests."""
    print("🚀 Assessment System Test Suite")
    print("Make sure the server is running on http://localhost:8000")
    print("=" * 50)
    
    try:
        success = test_assessment_system()
        if success:
            print("\n✅ All tests completed successfully!")
            print("\n📋 Test Summary:")
            print("   - Subject listing ✓")
            print("   - User registration ✓")
            print("   - User authentication ✓")
            print("   - Assessment start ✓")
            print("   - Assessment submission ✓")
            print("   - Recommendations retrieval ✓")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
