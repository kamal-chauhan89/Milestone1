"""
Startup script for Railway deployment
Checks if database exists and has data, if not populates it
"""

import os
import sys
import json
from fund_database import FundDatabase
from pathlib import Path

def check_and_populate_database():
    """Check if database exists and has data, populate if needed"""
    db_file = Path("mutual_funds_db.json")
    
    # Check if database file exists and has data
    if db_file.exists():
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if len(data) > 0:
                    print(f"✅ Database already exists with {len(data)} funds")
                    return True
        except Exception as e:
            print(f"⚠ Warning: Error reading existing database: {e}")
    
    # Database doesn't exist or is empty, create it
    print("📝 Database not found or empty, creating new one...")
    
    # Import and run populate script
    try:
        from populate_database import populate_database
        populate_database()
        print("✅ Database populated successfully")
        return True
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        return False

if __name__ == "__main__":
    if check_and_populate_database():
        print("✅ Startup completed successfully")
        # If running as startup script, exit normally
        if len(sys.argv) > 1 and sys.argv[1] == "startup":
            sys.exit(0)
    else:
        print("❌ Startup failed")
        sys.exit(1)