#!/usr/bin/env python3
"""
Simple database initialization script to create all tables.
This bypasses Alembic and creates the database schema directly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models import *  # Import all models

def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Verify the courses table has the url column
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        if 'courses' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('courses')]
            print(f"Courses table columns: {columns}")
            
            if 'url' in columns:
                print("✅ URL column found in courses table")
            else:
                print("❌ URL column NOT found in courses table")
        else:
            print("❌ Courses table not found")
            
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()
