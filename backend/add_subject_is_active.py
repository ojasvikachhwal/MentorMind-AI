#!/usr/bin/env python3
"""
Script to add is_active column to subjects table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from sqlalchemy import text

def add_is_active_column():
    """Add is_active column to subjects table"""
    db = SessionLocal()
    try:
        # Add the is_active column
        db.execute(text("ALTER TABLE subjects ADD COLUMN is_active BOOLEAN DEFAULT 1"))
        db.commit()
        print("Successfully added is_active column to subjects table")
        
        # Update existing subjects to be active
        db.execute(text("UPDATE subjects SET is_active = 1 WHERE is_active IS NULL"))
        db.commit()
        print("Updated existing subjects to be active")
        
    except Exception as e:
        print(f"Error adding column: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_is_active_column()
