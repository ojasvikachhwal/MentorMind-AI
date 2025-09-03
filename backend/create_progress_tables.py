#!/usr/bin/env python3
"""
Script to create progress tracking tables directly using SQLAlchemy.
This bypasses alembic for now to get the tables created.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base

def create_progress_tables():
    """Create all progress tracking tables."""
    print("Creating progress tracking tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Successfully created all progress tracking tables!")
        
        # Verify tables were created
        db = SessionLocal()
        try:
            # Check if tables exist by querying them
            result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%progress%' OR name LIKE '%coding%' OR name LIKE '%feedback%' OR name LIKE '%report%'")
            tables = result.fetchall()
            print(f"📊 Created tables: {[table[0] for table in tables]}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_progress_tables()
