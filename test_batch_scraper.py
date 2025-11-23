"""
Test script for batch scraper
Tests document parsing and link extraction before full scraping
"""

from document_link_parser import DocumentLinkParser
from batch_scraper import BatchMutualFundScraper
import json

def test_document_parsing():
    """Test if document can be parsed correctly"""
    print("=" * 60)
    print("TEST 1: Document Parsing")
    print("=" * 60)
    
    parser = DocumentLinkParser()
    doc_path = r"D:\download\Groww links for mutual funds.docx"
    
    try:
        print(f"\nParsing document: {doc_path}")
        links_data = parser.parse_document(doc_path)
        
        print(f"\n✅ Document parsed successfully!")
        print(f"   Total URLs found: {len(links_data['all_schemes'])}")
        
        if links_data.get('organized_by_amc'):
            print(f"   AMCs found: {len(links_data['organized_by_amc'])}")
            print(f"\n   First 5 AMCs:")
            for i, (amc, schemes) in enumerate(list(links_data['organized_by_amc'].items())[:5], 1):
                print(f"      {i}. {amc}: {len(schemes)} schemes")
        else:
            print("   ⚠️  No AMC organization detected")
        
        # Show sample URLs
        print(f"\n   Sample URLs (first 3):")
        for i, url in enumerate(links_data['all_schemes'][:3], 1):
            print(f"      {i}. {url}")
        
        # Save extracted links
        parser.save_extracted_links(links_data, 'test_extracted_links.json')
        print(f"\n   ✅ Links saved to: test_extracted_links.json")
        
        return links_data
        
    except FileNotFoundError:
        print(f"\n❌ Error: File not found: {doc_path}")
        print("   Please check the file path")
        return None
    except ImportError as e:
        print(f"\n❌ Error: Missing dependency")
        print(f"   {e}")
        print("   Install with: pip install python-docx")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_url_validation():
    """Test URL validation"""
    print("\n" + "=" * 60)
    print("TEST 2: URL Validation")
    print("=" * 60)
    
    parser = DocumentLinkParser()
    
    test_urls = [
        ("https://groww.in/mutual-funds/test-fund", True),
        ("https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth", True),
        ("https://groww.in/stocks/test", False),
        ("https://example.com/mutual-funds/test", False),
    ]
    
    all_valid = True
    for url, expected in test_urls:
        result = parser.validate_groww_url(url)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_valid = False
        print(f"   {status} {url[:50]}... -> {result}")
    
    if all_valid:
        print("\n   ✅ All URL validations passed!")
    else:
        print("\n   ⚠️  Some validations failed")
    
    return all_valid

def test_single_fund_scraping():
    """Test scraping a single fund"""
    print("\n" + "=" * 60)
    print("TEST 3: Single Fund Scraping")
    print("=" * 60)
    
    batch_scraper = BatchMutualFundScraper(delay_between_requests=1.0)
    
    # Test with a known fund
    test_url = "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth"
    
    print(f"\nTesting with: {test_url}")
    
    try:
        fund_data = batch_scraper.scraper.scrape_fund_page(test_url)
        
        if fund_data:
            print("\n   ✅ Successfully scraped fund data!")
            print(f"      Scheme Name: {fund_data.get('scheme_name', 'N/A')}")
            print(f"      NAV: {fund_data.get('nav', 'N/A')}")
            print(f"      Expense Ratio: {fund_data.get('expense_ratio', 'N/A')}")
            print(f"      Min SIP: {fund_data.get('minimum_investment', {}).get('min_sip', 'N/A')}")
            print(f"      Holdings: {len(fund_data.get('holdings', []))} items")
            
            # Validate
            validation = batch_scraper.scraper.validate_data(fund_data)
            print(f"\n   Validation Results:")
            for key, value in validation.items():
                status = "✅" if value else "❌"
                print(f"      {status} {key}: {value}")
            
            return True
        else:
            print("\n   ❌ Failed to scrape fund data")
            return False
            
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_scraping_small():
    """Test batch scraping with small number of URLs"""
    print("\n" + "=" * 60)
    print("TEST 4: Batch Scraping (Small Test)")
    print("=" * 60)
    
    # Load extracted links if available
    try:
        with open('test_extracted_links.json', 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    except FileNotFoundError:
        print("\n   ⚠️  No extracted links found. Run TEST 1 first.")
        return False
    
    if not links_data.get('all_schemes'):
        print("\n   ⚠️  No schemes found in extracted links")
        return False
    
    batch_scraper = BatchMutualFundScraper(delay_between_requests=1.5)
    
    # Test with first 3 schemes
    test_urls = links_data['all_schemes'][:3]
    print(f"\n   Testing with first {len(test_urls)} schemes...")
    
    try:
        results = batch_scraper.scrape_urls(test_urls)
        
        print(f"\n   ✅ Batch scraping test complete!")
        print(f"      Successful: {batch_scraper.stats['successful']}")
        print(f"      Failed: {batch_scraper.stats['failed']}")
        
        if results:
            batch_scraper.save_progress('test_scraped_data.json')
            print(f"      ✅ Test data saved to: test_scraped_data.json")
        
        return batch_scraper.stats['successful'] > 0
        
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("GROWW MUTUAL FUND SCRAPER - TEST SUITE")
    print("=" * 60)
    
    results = {
        'document_parsing': False,
        'url_validation': False,
        'single_fund': False,
        'batch_scraping': False,
    }
    
    # Test 1: Document Parsing
    links_data = test_document_parsing()
    results['document_parsing'] = links_data is not None
    
    # Test 2: URL Validation
    results['url_validation'] = test_url_validation()
    
    # Test 3: Single Fund Scraping
    results['single_fund'] = test_single_fund_scraping()
    
    # Test 4: Batch Scraping (only if previous tests passed)
    if results['document_parsing']:
        results['batch_scraping'] = test_batch_scraping_small()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name.replace('_', ' ').title()}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Ready for full scraping!")
    else:
        print("⚠️  SOME TESTS FAILED - Please fix issues before full scraping")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    main()

