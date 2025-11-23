"""
Automated Complete Scraper - No user input required
Scrapes all funds from the text file automatically
"""

from scrape_from_txt import CategoryAMCScraper
from batch_scraper import BatchMutualFundScraper
import json

def scrape_all_automated():
    """Automatically scrape all funds without user input"""
    print("=" * 60)
    print("GROWW MUTUAL FUND AUTOMATED SCRAPER")
    print("=" * 60)
    
    txt_file_path = r"C:\Users\sweet\projects\Groww links for mutual funds.txt"
    
    # Step 1: Load and extract all fund URLs
    print(f"\nStep 1: Loading links from: {txt_file_path}")
    category_scraper = CategoryAMCScraper()
    
    try:
        links_data = category_scraper.load_links_from_txt(txt_file_path)
        
        print(f"\n[OK] Links loaded:")
        print(f"   Category pages: {len(links_data['category_urls'])}")
        print(f"   AMC pages: {len(links_data['amc_urls'])}")
        
        # Step 2: Extract all individual fund URLs
        print(f"\nStep 2: Extracting all fund URLs from categories and AMCs...")
        all_fund_urls = category_scraper.extract_all_fund_urls(links_data)
        
        # Save extracted URLs
        category_scraper.save_fund_urls(all_fund_urls, 'all_extracted_fund_urls.json')
        
        if not all_fund_urls:
            print("\n[ERROR] No fund URLs found. Exiting.")
            return
        
        # Step 3: Start scraping
        print(f"\nStep 3: Starting to scrape {len(all_fund_urls)} funds...")
        print(f"   Estimated time: ~{len(all_fund_urls) * 2 / 60:.1f} minutes")
        print(f"   (2 seconds delay between requests)\n")
        
        batch_scraper = BatchMutualFundScraper(delay_between_requests=2.0)
        
        # Scrape all funds
        batch_scraper.scrape_urls(all_fund_urls)
        
        # Step 4: Save results
        print(f"\nStep 4: Saving results...")
        batch_scraper.save_progress('groww_all_funds_scraped.json')
        batch_scraper.print_summary()
        
        print("\n" + "=" * 60)
        print("[OK] SCRAPING COMPLETE!")
        print("=" * 60)
        print(f"\nOutput files:")
        print(f"   1. all_extracted_fund_urls.json - All extracted fund URLs")
        print(f"   2. groww_all_funds_scraped.json - Complete scraped data")
        print(f"\nTotal funds scraped: {batch_scraper.stats['successful']}")
        print(f"Failed: {batch_scraper.stats['failed']}")
        print(f"Skipped: {batch_scraper.stats['skipped']}")
        
    except FileNotFoundError:
        print(f"\n[ERROR] File not found: {txt_file_path}")
        print("   Please check the file path")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    scrape_all_automated()

