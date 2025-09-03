#!/usr/bin/env python3
"""
Admin initialization script to create the admin table and default admin user.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal, Base
from app.models import *  # Import all models including Admin
from app.core.admin_security import create_default_admin

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
