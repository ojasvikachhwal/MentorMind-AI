#!/usr/bin/env python3
"""
Simple admin initialization script to create the admin table and default admin user.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal, Base
from app.models import *  # Import all models including Admin

def hash_password(password: str) -> str:
    """Simple password hashing using bcrypt."""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_default_admin(db):
    """Create a default admin user if none exists."""
    from app.models.admin import Admin
    
    existing_admin = db.query(Admin).first()
    if not existing_admin:
        default_admin = Admin(
            username="admin",
            email="admin@mentormind.com",
            hashed_password=hash_password("password123"),
            is_active=True
        )
        db.add(default_admin)
        db.commit()
        db.refresh(default_admin)
        print(f"Default admin user created: admin / password123")
        return default_admin
    return existing_admin

def init_admin():
    """Initialize admin table and create default admin user."""
    print("🔐 Initializing Admin System...")
    
    try:
        # Create all tables (including admin table)
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Create default admin user
        print("👤 Creating default admin user...")
        db = SessionLocal()
        
        try:
            admin = create_default_admin(db)
            print(f"✅ Default admin user created/verified:")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Status: {'Active' if admin.is_active else 'Inactive'}")
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            raise
        finally:
            db.close()
            
        print("\n🎉 Admin system initialized successfully!")
        print("📝 Default credentials: admin / password123")
        print("⚠️  Remember to change the password in production!")
        
    except Exception as e:
        print(f"❌ Error initializing admin system: {e}")
        raise

if __name__ == "__main__":
    init_admin()
