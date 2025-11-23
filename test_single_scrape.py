"""
Quick test: Scrape a single fund and validate
"""

from comprehensive_scraper import ComprehensiveScraper
from fund_database import FundDatabase
import json

def test_single_fund():
    """Test scraping a single fund"""
    
    test_url = "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"
    
    print("="*80)
    print("TESTING SINGLE FUND SCRAPING")
    print("="*80)
    print(f"URL: {test_url}\n")
    
    # Initialize scraper
    scraper = ComprehensiveScraper(use_selenium=False)  # Use requests only for speed
    
    try:
        # Scrape fund
        fund_data = scraper.scrape_fund_data(test_url)
        
        print("\n" + "="*80)
        print("SCRAPED DATA")
        print("="*80)
        print(json.dumps(fund_data, indent=2, ensure_ascii=False))
        
        # Add to database
        db = FundDatabase()
        db.add_fund(fund_data)
        db.save_database()
        
        print("\n" + "="*80)
        print("✅ TEST COMPLETE")
        print("="*80)
        
        # Test query
        print("\nTesting database lookup:")
        found = db.find_by_name("HDFC Mid Cap")
        if found:
            print(f"✅ Found: {found['scheme_name']}")
            print(f"   Expense Ratio: {found['expense_ratio']}")
            print(f"   Exit Load: {found['exit_load']}")
            print(f"   Stamp Duty: {found['stamp_duty']}")
        
    finally:
        scraper.close()

if __name__ == "__main__":
    test_single_fund()
