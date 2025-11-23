"""
Scrape all mutual funds from links in the text file
Handles category pages and AMC pages to extract all individual fund URLs
"""

from groww_scraper import GrowwMutualFundScraper
from batch_scraper import BatchMutualFundScraper
import json
from typing import List, Set
from urllib.parse import urlparse


class CategoryAMCScraper:
    def __init__(self):
        self.scraper = GrowwMutualFundScraper()
        self.all_fund_urls: Set[str] = set()
        self.category_urls: List[str] = []
        self.amc_urls: List[str] = []
        
    def load_links_from_txt(self, file_path: str) -> dict:
        """Load and categorize links from text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        category_urls = []
        amc_urls = []
        other_urls = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Categorize URLs
            if '/category/' in line:
                category_urls.append(line)
            elif '/amc/' in line:
                amc_urls.append(line)
            elif '/top/' in line:
                category_urls.append(line)  # Top pages are like categories
            elif '/mutual-funds/' in line and not any(x in line for x in ['/category/', '/amc/', '/top/']):
                # Individual fund URL
                self.all_fund_urls.add(line)
            else:
                other_urls.append(line)
        
        self.category_urls = category_urls
        self.amc_urls = amc_urls
        
        return {
            'category_urls': category_urls,
            'amc_urls': amc_urls,
            'individual_funds': list(self.all_fund_urls),
            'other_urls': other_urls
        }
    
    def extract_funds_from_category(self, category_url: str) -> List[str]:
        """Extract all fund URLs from a category page"""
        print(f"  Extracting funds from category: {category_url}")
        fund_urls = self.scraper.get_fund_urls_from_category(category_url)
        return fund_urls
    
    def extract_funds_from_amc(self, amc_url: str) -> List[str]:
        """Extract all fund URLs from an AMC page"""
        print(f"  Extracting funds from AMC: {amc_url}")
        # AMC pages have similar structure to category pages
        # Use the same method but with a slight delay
        import time
        time.sleep(1)  # Small delay for AMC pages
        fund_urls = self.scraper.get_fund_urls_from_category(amc_url)
        return fund_urls
    
    def extract_all_fund_urls(self, links_data: dict) -> List[str]:
        """Extract all fund URLs from categories and AMCs"""
        print("\n" + "=" * 60)
        print("STEP 1: Extracting Individual Fund URLs")
        print("=" * 60)
        
        # Start with any individual fund URLs already in the file
        all_funds = list(self.all_fund_urls)
        print(f"\nFound {len(all_funds)} individual fund URLs in file")
        
        # Extract from category pages
        if links_data['category_urls']:
            print(f"\nProcessing {len(links_data['category_urls'])} category pages...")
            for i, category_url in enumerate(links_data['category_urls'], 1):
                print(f"\n[{i}/{len(links_data['category_urls'])}] {category_url}")
                try:
                    fund_urls = self.extract_funds_from_category(category_url)
                    for url in fund_urls:
                        if url not in all_funds:
                            all_funds.append(url)
                    print(f"  [OK] Found {len(fund_urls)} funds (Total: {len(all_funds)})")
                except Exception as e:
                    print(f"  [ERROR] Error: {e}")
        
        # Extract from AMC pages
        if links_data['amc_urls']:
            print(f"\nProcessing {len(links_data['amc_urls'])} AMC pages...")
            for i, amc_url in enumerate(links_data['amc_urls'], 1):
                print(f"\n[{i}/{len(links_data['amc_urls'])}] {amc_url}")
                try:
                    fund_urls = self.extract_funds_from_amc(amc_url)
                    for url in fund_urls:
                        if url not in all_funds:
                            all_funds.append(url)
                    print(f"  [OK] Found {len(fund_urls)} funds (Total: {len(all_funds)})")
                except Exception as e:
                    print(f"  [ERROR] Error: {e}")
        
        # Remove duplicates
        unique_funds = list(set(all_funds))
        
        print(f"\n{'=' * 60}")
        print(f"[OK] Total unique fund URLs extracted: {len(unique_funds)}")
        print(f"{'=' * 60}\n")
        
        return unique_funds
    
    def save_fund_urls(self, fund_urls: List[str], filename: str = 'all_fund_urls.json'):
        """Save extracted fund URLs to JSON"""
        data = {
            'total_funds': len(fund_urls),
            'extracted_at': self.scraper.scraped_data[0] if self.scraper.scraped_data else None,
            'fund_urls': fund_urls
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[SAVED] Fund URLs saved to: {filename}")


def main():
    """Main function to scrape all funds from text file"""
    print("=" * 60)
    print("GROWW MUTUAL FUND COMPLETE SCRAPER")
    print("=" * 60)
    
    txt_file_path = r"C:\Users\sweet\projects\Groww links for mutual funds.txt"
    
    # Step 1: Load and categorize links
    print(f"\nLoading links from: {txt_file_path}")
    category_scraper = CategoryAMCScraper()
    
    try:
        links_data = category_scraper.load_links_from_txt(txt_file_path)
        
        print(f"\n[OK] Links loaded:")
        print(f"   Category pages: {len(links_data['category_urls'])}")
        print(f"   AMC pages: {len(links_data['amc_urls'])}")
        print(f"   Individual funds: {len(links_data['individual_funds'])}")
        
        # Step 2: Extract all individual fund URLs
        all_fund_urls = category_scraper.extract_all_fund_urls(links_data)
        
        # Save extracted URLs
        category_scraper.save_fund_urls(all_fund_urls, 'all_extracted_fund_urls.json')
        
        if not all_fund_urls:
            print("\n[ERROR] No fund URLs found. Please check the links in the file.")
            return
        
        # Step 3: Ask user what to do
        print("\n" + "=" * 60)
        print("STEP 2: Scraping Options")
        print("=" * 60)
        print(f"\nFound {len(all_fund_urls)} individual fund URLs")
        print("\nOptions:")
        print("  1. Test with first 10 funds")
        print("  2. Scrape ALL funds (this will take time)")
        print("  3. Scrape first N funds (enter number)")
        print("  4. Save URLs only (skip scraping)")
        
        choice = input("\nEnter choice (1-4, default=1): ").strip() or "1"
        
        if choice == "4":
            print("\n[OK] URLs saved. Exiting.")
            return
        
        # Step 4: Start scraping
        batch_scraper = BatchMutualFundScraper(delay_between_requests=2.0)
        
        if choice == "1":
            print("\n[TEST] Testing with first 10 funds...")
            batch_scraper.scrape_urls(all_fund_urls, max_urls=10)
        elif choice == "2":
            print(f"\n[WARNING] This will scrape {len(all_fund_urls)} funds.")
            print(f"   Estimated time: ~{len(all_fund_urls) * 2 / 60:.1f} minutes")
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm == 'yes':
                print("\n[START] Starting full scraping...")
                batch_scraper.scrape_urls(all_fund_urls)
            else:
                print("Cancelled.")
                return
        elif choice == "3":
            try:
                n = int(input("Enter number of funds to scrape: ").strip())
                print(f"\nScraping first {n} funds...")
                batch_scraper.scrape_urls(all_fund_urls, max_urls=n)
            except ValueError:
                print("Invalid number")
                return
        
        # Step 5: Save results
        print("\n" + "=" * 60)
        print("STEP 3: Saving Results")
        print("=" * 60)
        
        batch_scraper.save_progress('groww_all_funds_scraped.json')
        batch_scraper.print_summary()
        
        print("\n[OK] Scraping complete!")
        print(f"Check 'groww_all_funds_scraped.json' for all scraped data")
        
    except FileNotFoundError:
        print(f"\n[ERROR] Error: File not found: {txt_file_path}")
        print("   Please check the file path")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

