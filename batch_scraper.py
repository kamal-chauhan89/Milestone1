"""
Batch Scraper for Groww Mutual Funds
Uses links from document to scrape all AMCs and schemes
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from groww_scraper import GrowwMutualFundScraper
from document_link_parser import DocumentLinkParser


class BatchMutualFundScraper:
    def __init__(self, delay_between_requests: float = 2.0):
        self.scraper = GrowwMutualFundScraper()
        self.parser = DocumentLinkParser()
        self.delay = delay_between_requests
        self.scraped_data = []
        self.failed_urls = []
        self.stats = {
            'total_urls': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
        }
    
    def load_links_from_document(self, doc_path: str) -> Dict[str, List[str]]:
        """Load links from document file"""
        print(f"Loading links from: {doc_path}")
        links_data = self.parser.parse_document(doc_path)
        return links_data
    
    def load_links_from_json(self, json_path: str) -> Dict[str, List[str]]:
        """Load links from previously extracted JSON file"""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def scrape_urls(self, urls: List[str], start_index: int = 0, max_urls: Optional[int] = None) -> List[Dict]:
        """Scrape multiple URLs"""
        if max_urls:
            urls = urls[start_index:start_index + max_urls]
        else:
            urls = urls[start_index:]
        
        self.stats['total_urls'] = len(urls)
        
        print(f"\n{'='*60}")
        print(f"Starting batch scraping: {len(urls)} URLs")
        print(f"{'='*60}\n")
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Processing: {url}")
            
            try:
                fund_data = self.scraper.scrape_fund_page(url)
                
                if fund_data:
                    # Validate data
                    validation = self.scraper.validate_data(fund_data)
                    
                    if validation.get('has_scheme_name') or validation.get('has_minimum_data'):
                        self.scraped_data.append(fund_data)
                        self.stats['successful'] += 1
                        print(f"  ✅ Success: {fund_data.get('scheme_name', 'Unknown')}")
                    else:
                        self.stats['skipped'] += 1
                        print(f"  ⚠️  Skipped: Insufficient data")
                        self.failed_urls.append({
                            'url': url,
                            'reason': 'Insufficient data',
                            'timestamp': datetime.now().isoformat()
                        })
                else:
                    self.stats['failed'] += 1
                    print(f"  ❌ Failed: Could not scrape")
                    self.failed_urls.append({
                        'url': url,
                        'reason': 'Scraping failed',
                        'timestamp': datetime.now().isoformat()
                    })
            
            except Exception as e:
                self.stats['failed'] += 1
                print(f"  ❌ Error: {str(e)}")
                self.failed_urls.append({
                    'url': url,
                    'reason': f'Exception: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Delay between requests
            if i < len(urls):
                time.sleep(self.delay)
        
        return self.scraped_data
    
    def scrape_by_amc(self, links_data: Dict[str, List[str]], amc_name: Optional[str] = None):
        """Scrape schemes organized by AMC"""
        organized = links_data.get('organized_by_amc', {})
        
        if not organized:
            print("⚠️  No AMC organization found. Scraping all schemes...")
            return self.scrape_urls(links_data['all_schemes'])
        
        if amc_name:
            # Scrape specific AMC
            if amc_name in organized:
                print(f"Scraping schemes for AMC: {amc_name}")
                return self.scrape_urls(organized[amc_name])
            else:
                print(f"❌ AMC '{amc_name}' not found")
                print(f"Available AMCs: {list(organized.keys())}")
                return []
        
        # Scrape all AMCs
        all_scraped = []
        for amc, schemes in organized.items():
            print(f"\n{'='*60}")
            print(f"Scraping AMC: {amc} ({len(schemes)} schemes)")
            print(f"{'='*60}")
            
            amc_data = self.scrape_urls(schemes)
            all_scraped.extend(amc_data)
            
            # Save progress after each AMC
            self.save_progress(amc_name=amc)
        
        return all_scraped
    
    def save_progress(self, filename: str = None, amc_name: str = None):
        """Save scraped data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if amc_name:
                # Sanitize AMC name for filename
                safe_name = "".join(c for c in amc_name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_')
                filename = f'groww_scraped_{safe_name}_{timestamp}.json'
            else:
                filename = f'groww_scraped_all_{timestamp}.json'
        
        output = {
            'metadata': {
                'scraped_at': datetime.now().isoformat(),
                'total_schemes': len(self.scraped_data),
                'stats': self.stats,
            },
            'schemes': self.scraped_data,
            'failed_urls': self.failed_urls
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Progress saved to: {filename}")
        print(f"   Successful: {self.stats['successful']}")
        print(f"   Failed: {self.stats['failed']}")
        print(f"   Skipped: {self.stats['skipped']}")
    
    def print_summary(self):
        """Print scraping summary"""
        print(f"\n{'='*60}")
        print("SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total URLs: {self.stats['total_urls']}")
        print(f"✅ Successful: {self.stats['successful']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"⚠️  Skipped: {self.stats['skipped']}")
        print(f"Success Rate: {(self.stats['successful']/self.stats['total_urls']*100):.1f}%" if self.stats['total_urls'] > 0 else "N/A")
        print(f"{'='*60}\n")


def main():
    """Main function to run batch scraping"""
    batch_scraper = BatchMutualFundScraper(delay_between_requests=2.0)
    
    # Option 1: Load from document
    doc_path = r"D:\download\Groww links for mutual funds.docx"
    
    # Option 2: Load from previously extracted JSON
    # json_path = "groww_all_scheme_links.json"
    
    try:
        # Load links from document
        print("Step 1: Extracting links from document...")
        links_data = batch_scraper.load_links_from_document(doc_path)
        
        # Save extracted links for reference
        batch_scraper.parser.save_extracted_links(links_data, 'groww_all_scheme_links.json')
        
        print(f"\nStep 2: Starting batch scraping...")
        print(f"Total schemes to scrape: {len(links_data['all_schemes'])}")
        
        # Ask user for preference
        print("\nScraping options:")
        print("1. Scrape all schemes")
        print("2. Scrape by AMC (organized)")
        print("3. Scrape specific AMC")
        print("4. Scrape first N schemes (for testing)")
        
        choice = input("\nEnter choice (1-4, default=1): ").strip() or "1"
        
        if choice == "1":
            # Scrape all
            batch_scraper.scrape_urls(links_data['all_schemes'])
        elif choice == "2":
            # Scrape by AMC
            batch_scraper.scrape_by_amc(links_data)
        elif choice == "3":
            # Scrape specific AMC
            organized = links_data.get('organized_by_amc', {})
            if organized:
                print(f"\nAvailable AMCs:")
                for i, amc in enumerate(organized.keys(), 1):
                    print(f"  {i}. {amc}")
                amc_name = input("\nEnter AMC name: ").strip()
                batch_scraper.scrape_by_amc(links_data, amc_name)
            else:
                print("No AMC organization found")
        elif choice == "4":
            # Test with first N
            n = input("Enter number of schemes to scrape (default=5): ").strip()
            n = int(n) if n.isdigit() else 5
            batch_scraper.scrape_urls(links_data['all_schemes'], max_urls=n)
        
        # Save final results
        batch_scraper.save_progress()
        batch_scraper.print_summary()
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"Please check the file path: {doc_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

