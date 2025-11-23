"""
Complete Setup Script for FAQ Assistant Backend
Runs all setup steps in sequence
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath):
    """Check if file exists"""
    return Path(filepath).exists()

def main():
    print("=" * 60)
    print("FAQ ASSISTANT BACKEND - SETUP")
    print("=" * 60)
    
    # Step 1: Check if scraped data exists
    print("\nStep 1: Checking for scraped data...")
    scraped_file = "groww_all_funds_scraped.json"
    
    if not check_file_exists(scraped_file):
        print(f"  [WARNING] {scraped_file} not found")
        print("  You need to run the scraper first:")
        print("    python scrape_all_automated.py")
        print("\n  Would you like to continue anyway? (y/n): ", end="")
        choice = input().strip().lower()
        if choice != 'y':
            print("  Setup cancelled.")
            return
    else:
        print(f"  [OK] Found {scraped_file}")
    
    # Step 2: Store data
    print("\nStep 2: Storing scraped data...")
    try:
        from data_storage import MutualFundDataStore
        
        store = MutualFundDataStore(data_dir="data")
        
        if check_file_exists(scraped_file):
            schemes = store.load_scraped_data(scraped_file)
            print(f"  Loading {len(schemes)} schemes...")
            store.store_schemes(schemes)
            print("  [OK] Data stored successfully")
        else:
            print("  [SKIP] No scraped data to store")
    
    except Exception as e:
        print(f"  [ERROR] {e}")
        return
    
    # Step 3: Test FAQ assistant
    print("\nStep 3: Testing FAQ assistant...")
    try:
        from faq_assistant_backend import FAQAssistant
        
        assistant = FAQAssistant()
        print(f"  [OK] Loaded {len(assistant.schemes)} schemes")
        
        # Quick test
        test_query = "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"
        result = assistant.answer_query(test_query)
        
        if result.get('answer'):
            print(f"  [OK] Test query answered successfully")
            print(f"  Query: {test_query}")
            print(f"  Answer: {result['answer'][:80]}...")
        else:
            print("  [WARNING] Test query failed")
    
    except Exception as e:
        print(f"  [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Check dependencies
    print("\nStep 4: Checking dependencies...")
    try:
        import flask
        import flask_cors
        print("  [OK] Flask and Flask-CORS installed")
    except ImportError:
        print("  [WARNING] Flask not installed")
        print("  Install with: pip install flask flask-cors")
    
    # Summary
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Test the backend:")
    print("     python faq_assistant_backend.py")
    print("\n  2. Start the API server:")
    print("     python api_server.py")
    print("\n  3. Test API (in another terminal):")
    print('     curl -X POST http://localhost:5000/query \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"}\'')
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

