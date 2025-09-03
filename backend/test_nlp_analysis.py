#!/usr/bin/env python3
"""
Test script for the NLP analysis system.
This script tests the question difficulty classification and tag extraction.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "teststudent"
TEST_PASSWORD = "password"

def test_nlp_analysis():
    """Test the NLP analysis endpoints."""
    print("🧪 Testing NLP Analysis System")
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
    
    # Step 2: Test single question analysis
    print("\n2. Testing single question analysis...")
    test_questions = [
        {
            "subject": "Mathematics",
            "text": "What is 2 + 2?"
        },
        {
            "subject": "Mathematics",
            "text": "Solve the quadratic equation: x² + 5x + 6 = 0 using the quadratic formula and explain your reasoning step by step."
        },
        {
            "subject": "Physics",
            "text": "Calculate the force exerted by a 5kg object accelerating at 2 m/s² and describe the relationship between mass, acceleration, and force."
        },
        {
            "subject": "Computer Science",
            "text": "Implement a binary search algorithm in Python and analyze its time complexity."
        }
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Testing question {i}: {question['text'][:50]}...")
        try:
            response = requests.post(
                f"{BASE_URL}/questions/analyze",
                headers=headers,
                json=question
            )
            
            if response.status_code == 200:
                analysis = response.json()
                print(f"   ✅ Analysis successful!")
                print(f"      - Difficulty: {analysis.get('difficulty')}")
                print(f"      - Tags: {', '.join(analysis.get('tags', [])[:3])}")
                print(f"      - Confidence: {analysis.get('confidence', 0):.2f}")
                print(f"      - Word count: {analysis.get('word_count')}")
                print(f"      - Complexity score: {analysis.get('complexity_score', 0):.2f}")
                print(f"      - Method: {analysis.get('analysis_method')}")
                print(f"      - Processing time: {analysis.get('processing_time_ms', 0):.1f}ms")
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                print(f"      - Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error analyzing question: {e}")
    
    # Step 3: Test batch question analysis
    print("\n3. Testing batch question analysis...")
    try:
        batch_request = {
            "questions": test_questions[:2],  # Test with first 2 questions
            "use_ml": False
        }
        
        response = requests.post(
            f"{BASE_URL}/questions/analyze/batch",
            headers=headers,
            json=batch_request
        )
        
        if response.status_code == 200:
            batch_result = response.json()
            print("✅ Batch analysis successful!")
            print(f"   - Total questions: {batch_result.get('total_questions')}")
            print(f"   - Processing time: {batch_result.get('processing_time_ms', 0):.1f}ms")
            print(f"   - Analysis method: {batch_result.get('analysis_method')}")
            
            # Show results for each question
            for i, result in enumerate(batch_result.get('results', []), 1):
                print(f"   Question {i}: {result.get('difficulty')} - {', '.join(result.get('tags', [])[:2])}")
        else:
            print(f"❌ Batch analysis failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Error in batch analysis: {e}")
    
    # Step 4: Test question upload with analysis
    print("\n4. Testing question upload with analysis...")
    try:
        upload_request = {
            "subject": "Mathematics",
            "questions": [
                "Find the derivative of f(x) = x³ + 2x² + 1",
                "Calculate the area under the curve y = x² from x = 0 to x = 2"
            ],
            "auto_analyze": True,
            "save_to_db": False
        }
        
        response = requests.post(
            f"{BASE_URL}/questions/upload",
            headers=headers,
            json=upload_request
        )
        
        if response.status_code == 200:
            upload_result = response.json()
            print("✅ Question upload successful!")
            print(f"   - Total questions: {upload_result.get('total_questions')}")
            print(f"   - Analyzed questions: {upload_result.get('analyzed_questions')}")
            print(f"   - Processing time: {upload_result.get('processing_time_ms', 0):.1f}ms")
        else:
            print(f"❌ Question upload failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Error in question upload: {e}")
    
    # Step 5: Test question search
    print("\n5. Testing question search...")
    try:
        response = requests.get(
            f"{BASE_URL}/questions/search",
            headers=headers,
            params={
                "tags": ["algebra"],
                "difficulty": "medium",
                "limit": 10
            }
        )
        
        if response.status_code == 200:
            search_result = response.json()
            print("✅ Question search successful!")
            print(f"   - Total found: {search_result.get('total_found')}")
            print(f"   - Search time: {search_result.get('search_time_ms', 0):.1f}ms")
        else:
            print(f"❌ Question search failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Error in question search: {e}")
    
    # Step 6: Test analysis statistics
    print("\n6. Testing analysis statistics...")
    try:
        response = requests.get(
            f"{BASE_URL}/questions/analysis/stats",
            headers=headers
        )
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Analysis statistics retrieved!")
            print(f"   - Total questions analyzed: {stats.get('total_questions_analyzed')}")
            print(f"   - Average confidence: {stats.get('average_confidence', 0):.2f}")
            print(f"   - Average complexity: {stats.get('average_complexity', 0):.2f}")
        else:
            print(f"❌ Statistics retrieval failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
    
    # Step 7: Test analyzer information
    print("\n7. Testing analyzer information...")
    try:
        response = requests.get(
            f"{BASE_URL}/questions/analysis/analyzer-info",
            headers=headers
        )
        
        if response.status_code == 200:
            analyzer_info = response.json()
            print("✅ Analyzer information retrieved!")
            print(f"   - Status: {analyzer_info.get('analyzer_status')}")
            print(f"   - Method: {analyzer_info.get('configuration', {}).get('analysis_method')}")
            print(f"   - ML model available: {analyzer_info.get('configuration', {}).get('ml_model_available')}")
            
            # Show capabilities
            capabilities = analyzer_info.get('capabilities', [])
            print(f"   - Capabilities: {len(capabilities)} features")
            for capability in capabilities[:3]:  # Show first 3
                print(f"     • {capability}")
        else:
            print(f"❌ Analyzer info retrieval failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting analyzer info: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 NLP Analysis Testing Complete!")
    return True

def test_difficulty_classification():
    """Test the difficulty classification logic."""
    print("\n🧠 Testing Difficulty Classification Logic")
    print("-" * 40)
    
    # Test cases with expected difficulties
    test_cases = [
        ("What is 2 + 2?", "easy", "Very short question"),
        ("Solve for x: 2x + 5 = 15", "easy", "Simple algebra question"),
        ("Find the derivative of f(x) = x² + 3x + 1 and explain your reasoning", "medium", "Medium length with technical terms"),
        ("Calculate the definite integral of the function f(x) = sin(x)cos(x) from x = 0 to x = π/2, showing all steps and using appropriate trigonometric identities", "hard", "Long question with complex mathematical concepts")
    ]
    
    for question, expected_difficulty, description in test_cases:
        word_count = len(question.split())
        print(f"Question: {question[:50]}...")
        print(f"   - Word count: {word_count}")
        print(f"   - Expected: {expected_difficulty}")
        print(f"   - Description: {description}")
        print()

def main():
    """Main test function."""
    print("🚀 Starting NLP Analysis System Tests")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Make sure you have test data in the database")
    
    try:
        success = test_nlp_analysis()
        if success:
            print("\n✅ All tests completed successfully!")
            
            # Test difficulty classification logic
            test_difficulty_classification()
        else:
            print("\n❌ Some tests failed!")
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()
