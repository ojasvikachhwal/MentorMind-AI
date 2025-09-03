#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI application setup.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported successfully."""
    try:
        from app.main import app
        from app.models import User
        from app.schemas import UserCreate, UserResponse, Token
        from app.database import get_db
        from app.auth import get_current_user, create_access_token
        from app.routes import router
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test if the FastAPI app can be created."""
    try:
        from app.main import app
        print(f"✅ FastAPI app created successfully!")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing FastAPI Application Setup...")
    print("=" * 50)
    
    success = True
    
    # Test imports
    print("\n1. Testing imports...")
    if not test_imports():
        success = False
    
    # Test app creation
    print("\n2. Testing app creation...")
    if not test_app_creation():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your FastAPI application is ready to run.")
        print("\nTo start the application, run:")
        print("   uvicorn app.main:app --reload")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
