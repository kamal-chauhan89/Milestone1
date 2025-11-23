"""
Batch URL Scraper for Groww Mutual Funds
Scrapes all URLs from the Groww links file and extracts comprehensive data
"""

import json
import time
from pathlib import Path
from typing import List, Dict
from groww_scraper import GrowwMutualFundScraper
from datetime import datetime


class BatchURLScraper:
    def __init__(self, urls_file: str = "Groww links for mutual funds.txt"):
        self.scraper = GrowwMutualFundScraper()
        self.urls_file = urls_file
        self.output_dir = Path("scraped_data")
        self.output_dir.mkdir(exist_ok=True)
        
    def load_urls(self) -> List[str]:
        """Load URLs from the text file"""
        urls = []
        try:
            with open(self.urls_file, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and url.startswith('http'):
                        urls.append(url)
        except FileNotFoundError:
            print(f"Error: {self.urls_file} not found!")
            return []
        
        return urls
    
    def scrape_category_or_amc_page(self, url: str) -> List[str]:
        """Extract fund URLs from category or AMC pages"""
        print(f"\n{'='*80}")
        print(f"Extracting fund URLs from: {url}")
        print(f"{'='*80}")
        
        fund_urls = self.scraper.get_fund_urls_from_category(url)
        print(f"Found {len(fund_urls)} fund URLs")
        
        return fund_urls
    
    def scrape_all_funds_from_url(self, category_url: str) -> List[Dict]:
        """Scrape all funds from a category/AMC page"""
        fund_urls = self.scrape_category_or_amc_page(category_url)
        
        all_funds_data = []
        
        for i, fund_url in enumerate(fund_urls, 1):
            print(f"\n[{i}/{len(fund_urls)}] Scraping: {fund_url}")
            
            try:
                fund_data = self.scraper.scrape_fund_page(fund_url)
                
                if fund_data:
                    # Validate data
                    if self.validate_fund_data(fund_data):
                        all_funds_data.append(fund_data)
                        print(f"✓ Successfully scraped: {fund_data.get('scheme_name', 'Unknown')}")
                    else:
                        print(f"⚠ Validation failed for: {fund_url}")
                else:
                    print(f"✗ Failed to scrape: {fund_url}")
                
                # Rate limiting - be respectful to the server
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping {fund_url}: {e}")
                continue
        
        return all_funds_data
    
    def validate_fund_data(self, fund_data: Dict) -> bool:
        """Validate scraped fund data"""
        # Check required fields
        if not fund_data.get('source_url'):
            return False
        
        if not self.scraper.validate_url(fund_data['source_url']):
            return False
        
        if not fund_data.get('scheme_name'):
            return False
        
        # Check if we got at least some useful data
        has_data = any([
            fund_data.get('expense_ratio'),
            fund_data.get('exit_load'),
            fund_data.get('nav'),
            fund_data.get('riskometer'),
        ])
        
        return has_data
    
    def scrape_all_categories(self) -> Dict[str, List[Dict]]:
        """Scrape all categories from the URLs file"""
        urls = self.load_urls()
        
        if not urls:
            print("No URLs found!")
            return {}
        
        print(f"\n{'='*80}")
        print(f"BATCH SCRAPING STARTED")
        print(f"{'='*80}")
        print(f"Total URLs to process: {len(urls)}")
        print(f"Output directory: {self.output_dir}")
        
        all_scraped_data = {}
        
        for i, url in enumerate(urls, 1):
            print(f"\n\n{'#'*80}")
            print(f"# Processing URL {i}/{len(urls)}")
            print(f"{'#'*80}")
            
            try:
                # Extract category/AMC name from URL
                category_name = url.split('/')[-1].replace('best-', '').replace('-mutual-funds', '')
                
                # Scrape all funds from this URL
                funds_data = self.scrape_all_funds_from_url(url)
                
                if funds_data:
                    all_scraped_data[category_name] = funds_data
                    
                    # Save intermediate results
                    self.save_category_data(category_name, funds_data)
                    print(f"\n✓ Saved {len(funds_data)} funds for category: {category_name}")
                
            except Exception as e:
                print(f"\nError processing {url}: {e}")
                continue
        
        return all_scraped_data
    
    def save_category_data(self, category_name: str, funds_data: List[Dict]):
        """Save data for a specific category"""
        filename = self.output_dir / f"{category_name}_funds.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(funds_data, f, indent=2, ensure_ascii=False)
    
    def consolidate_all_data(self):
        """Consolidate all scraped data into a single file"""
        all_funds = []
        
        for json_file in self.output_dir.glob("*_funds.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    funds = json.load(f)
                    all_funds.extend(funds)
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
        
        # Remove duplicates based on source URL
        seen_urls = set()
        unique_funds = []
        
        for fund in all_funds:
            url = fund.get('source_url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_funds.append(fund)
        
        # Save consolidated data
        consolidated_file = self.output_dir / "all_funds_consolidated.json"
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(unique_funds, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"CONSOLIDATION COMPLETE")
        print(f"{'='*80}")
        print(f"Total unique funds: {len(unique_funds)}")
        print(f"Saved to: {consolidated_file}")
        
        return unique_funds
    
    def generate_summary_report(self, all_funds: List[Dict]):
        """Generate a summary report of scraped data"""
        report = {
            'total_funds': len(all_funds),
            'scraped_at': datetime.now().isoformat(),
            'categories': {},
            'data_completeness': {
                'with_expense_ratio': 0,
                'with_exit_load': 0,
                'with_stamp_duty': 0,
                'with_tax_implications': 0,
                'with_holdings': 0,
                'with_riskometer': 0,
            }
        }
        
        for fund in all_funds:
            # Count data completeness
            if fund.get('expense_ratio'):
                report['data_completeness']['with_expense_ratio'] += 1
            if fund.get('exit_load'):
                report['data_completeness']['with_exit_load'] += 1
            if fund.get('stamp_duty'):
                report['data_completeness']['with_stamp_duty'] += 1
            if fund.get('tax_implications'):
                report['data_completeness']['with_tax_implications'] += 1
            if fund.get('holdings') and len(fund['holdings']) > 0:
                report['data_completeness']['with_holdings'] += 1
            if fund.get('riskometer'):
                report['data_completeness']['with_riskometer'] += 1
        
        # Save report
        report_file = self.output_dir / "scraping_summary.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*80}")
        print(f"Total Funds: {report['total_funds']}")
        print(f"\nData Completeness:")
        for key, value in report['data_completeness'].items():
            percentage = (value / report['total_funds'] * 100) if report['total_funds'] > 0 else 0
            print(f"  {key.replace('_', ' ').title()}: {value} ({percentage:.1f}%)")
        print(f"\nReport saved to: {report_file}")


def main():
    """Main execution"""
    print("="*80)
    print("GROWW MUTUAL FUNDS BATCH SCRAPER")
    print("="*80)
    
    scraper = BatchURLScraper()
    
    # Scrape all categories
    all_data = scraper.scrape_all_categories()
    
    # Consolidate data
    unique_funds = scraper.consolidate_all_data()
    
    # Generate summary report
    scraper.generate_summary_report(unique_funds)
    
    print("\n" + "="*80)
    print("✅ BATCH SCRAPING COMPLETED!")
    print("="*80)


if __name__ == "__main__":
    main()
