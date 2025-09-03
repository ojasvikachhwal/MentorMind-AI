#!/usr/bin/env python3
"""
Create a test user for testing the progress tracking system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_test_user():
    """Create a test user for testing purposes"""
    print("👤 Creating test user...")
    
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.username == "teststudent").first()
        if existing_user:
            print(f"✅ Test user already exists: {existing_user.username}")
            return existing_user
        
        # Create new test user
        test_user = User(
            username="teststudent",
            email="test@mentormind.com",
            hashed_password=get_password_hash("testpass123"),
            full_name="Test Student",
            bio="Test user for progress tracking system",
            is_active=True,
            is_verified=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ Created test user: {test_user.username} (ID: {test_user.id})")
        return test_user
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
