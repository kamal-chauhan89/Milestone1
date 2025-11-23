"""
Test script for Groww Mutual Fund Scraper
Tests the scraper on example fund pages
"""

from groww_scraper import GrowwMutualFundScraper
import json

def test_single_fund():
    """Test scraping a single fund"""
    print("=" * 60)
    print("TEST 1: Single Fund Scraping")
    print("=" * 60)
    
    scraper = GrowwMutualFundScraper()
    
    test_urls = [
        "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth",
        "https://groww.in/mutual-funds/axis-floater-fund-direct-growth",
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        fund_data = scraper.scrape_fund_page(url)
        
        if fund_data:
            print("\n✅ Successfully scraped data:")
            print(f"  Scheme Name: {fund_data.get('scheme_name')}")
            print(f"  NAV: {fund_data.get('nav')}")
            print(f"  Expense Ratio: {fund_data.get('expense_ratio')}")
            print(f"  Min SIP: {fund_data.get('minimum_investment', {}).get('min_sip')}")
            print(f"  Riskometer: {fund_data.get('riskometer')}")
            print(f"  Benchmark: {fund_data.get('benchmark')}")
            print(f"  Holdings Count: {len(fund_data.get('holdings', []))}")
            
            # Validate
            validation = scraper.validate_data(fund_data)
            print("\nValidation Results:")
            for key, value in validation.items():
                status = "✅" if value else "❌"
                print(f"  {status} {key}: {value}")
        else:
            print("❌ Failed to scrape data")
        
        print("\n" + "-" * 60)

def test_url_validation():
    """Test URL validation"""
    print("\n" + "=" * 60)
    print("TEST 2: URL Validation")
    print("=" * 60)
    
    scraper = GrowwMutualFundScraper()
    
    test_urls = [
        ("https://groww.in/mutual-funds/test-fund", True),
        ("https://groww.in/mutual-funds/category/best-large-cap-mutual-funds", True),
        ("https://example.com/mutual-funds/test", False),
        ("https://groww.in/stocks/test", False),
        ("", False),
    ]
    
    for url, expected in test_urls:
        result = scraper.validate_url(url)
        status = "✅" if result == expected else "❌"
        print(f"{status} {url}: {result} (expected: {expected})")

def test_category_scraping():
    """Test category page scraping"""
    print("\n" + "=" * 60)
    print("TEST 3: Category Page Scraping")
    print("=" * 60)
    
    scraper = GrowwMutualFundScraper()
    
    category_url = "https://groww.in/mutual-funds/category/best-banking-and-psu-mutual-funds"
    print(f"Fetching fund URLs from: {category_url}")
    
    fund_urls = scraper.get_fund_urls_from_category(category_url)
    print(f"\nFound {len(fund_urls)} fund URLs")
    
    if fund_urls:
        print("\nFirst 5 URLs:")
        for i, url in enumerate(fund_urls[:5], 1):
            print(f"  {i}. {url}")
    else:
        print("⚠️  No fund URLs found")

def test_data_extraction():
    """Test specific data extraction methods"""
    print("\n" + "=" * 60)
    print("TEST 4: Data Extraction Methods")
    print("=" * 60)
    
    scraper = GrowwMutualFundScraper()
    url = "https://groww.in/mutual-funds/axis-floater-fund-direct-growth"
    
    print(f"Testing extraction from: {url}")
    soup = scraper.get_page(url)
    
    if soup:
        print("\nExtracting specific fields:")
        
        # Test minimum investment extraction
        min_inv = scraper.extract_minimum_investment(soup)
        print(f"  Minimum Investment: {json.dumps(min_inv, indent=4)}")
        
        # Test sector allocation
        sectors = scraper.extract_sector_allocation(soup)
        print(f"  Sector Allocation: {json.dumps(sectors, indent=4)}")
        
        # Test holdings
        holdings = scraper.extract_holdings(soup)
        print(f"  Holdings Count: {len(holdings)}")
        if holdings:
            print(f"  First Holding: {json.dumps(holdings[0], indent=4)}")
        
        # Test debt/cash analysis
        analysis = scraper.extract_debt_cash_analysis(soup)
        print(f"  Debt/Cash Analysis: {json.dumps(analysis, indent=4)}")
    else:
        print("❌ Failed to fetch page")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GROWW MUTUAL FUND SCRAPER - TEST SUITE")
    print("=" * 60)
    
    # Run tests
    test_url_validation()
    test_single_fund()
    test_category_scraping()
    test_data_extraction()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)

