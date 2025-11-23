"""
Populate database with fund data
"""

from comprehensive_scraper import ComprehensiveScraper
from fund_database import FundDatabase
from url_loader import URLLoader
import time

def populate_database():
    """Populate database with fund data"""
    print("="*80)
    print("POPULATING DATABASE WITH FUND DATA")
    print("="*80)
    
    # Initialize scraper and database
    scraper = ComprehensiveScraper(use_selenium=False)  # Use requests for speed
    database = FundDatabase()
    
    # Test URLs - direct fund pages
    test_urls = [
        "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
        "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
        "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        "https://groww.in/mutual-funds/hdfc-bluechip-fund-direct-growth"
    ]
    
    try:
        # Scrape each fund
        for i, url in enumerate(test_urls, 1):
            print(f"\n[{i}/{len(test_urls)}] Scraping: {url}")
            
            fund_data = scraper.scrape_fund_data(url)
            
            if fund_data and fund_data.get("scheme_name") != "Information not available":
                database.add_fund(fund_data)
                print(f"✅ Added: {fund_data['scheme_name']}")
            else:
                print(f"❌ Failed to scrape valid data from: {url}")
            
            # Rate limiting
            time.sleep(2)
        
        # Save database
        database.save_database()
        
        # Show statistics
        print("\n" + "="*80)
        print("DATABASE POPULATED SUCCESSFULLY")
        print("="*80)
        stats = database.get_statistics()
        print(f"Total funds: {stats['total_funds']}")
        print("\nData completeness:")
        for field, data in stats['field_completeness'].items():
            print(f"  {field}: {data['available']} ({data['percentage']:.1f}%)")
            
        # Show sample funds
        print("\nSample funds in database:")
        funds = database.get_all_funds()
        for fund in funds[:3]:
            print(f"  - {fund['scheme_name']}")
            print(f"    Expense Ratio: {fund['expense_ratio']}")
            print(f"    Exit Load: {fund['exit_load']}")
            print(f"    Source: {fund['source_url']}")
            print()
        
    finally:
        scraper.close()

if __name__ == "__main__":
    populate_database()
