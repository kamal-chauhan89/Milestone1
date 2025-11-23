"""
Quick test: Scrape HDFC AMC funds and validate data
"""

from batch_url_scraper import BatchURLScraper
from data_storage import MutualFundDataStore
import json

def test_hdfc_amc_scraping():
    """Test scraping HDFC AMC"""
    scraper = BatchURLScraper()
    
    # Test with HDFC AMC
    hdfc_url = "https://groww.in/mutual-funds/amc/hdfc-mutual-funds"
    
    print("="*80)
    print("TESTING HDFC AMC SCRAPING")
    print("="*80)
    
    # Scrape HDFC funds
    hdfc_funds = scraper.scrape_all_funds_from_url(hdfc_url)
    
    if hdfc_funds:
        print(f"\n✅ Successfully scraped {len(hdfc_funds)} HDFC funds")
        
        # Save to file
        scraper.save_category_data("hdfc-amc", hdfc_funds)
        
        # Store in database
        store = MutualFundDataStore()
        normalized = store.store_schemes(hdfc_funds)
        
        # Show sample
        print("\n" + "="*80)
        print("SAMPLE FUND DATA")
        print("="*80)
        
        if normalized:
            sample = normalized[0]
            print(f"\nScheme: {sample['scheme_name']}")
            print(f"URL: {sample['source_url']}")
            print(f"\nFacts:")
            for key, value in sample['facts'].items():
                if value:
                    print(f"  - {key}: {value}")
            
            print(f"\nHoldings: {len(sample.get('holdings', []))} found")
        
        return True
    else:
        print("\n❌ No funds scraped")
        return False

if __name__ == "__main__":
    test_hdfc_amc_scraping()
