"""
Comprehensive Scraper for Groww Mutual Funds
Uses requests + BeautifulSoup for static content, Selenium for JS-rendered pages
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from typing import Dict, Optional, List
from url_loader import URLLoader
from fund_database import FundDatabase


class ComprehensiveScraper:
    """Scrapes mutual fund data from Groww using requests and Selenium"""
    
    def __init__(self, use_selenium: bool = True):
        self.use_selenium = use_selenium
        self.driver = None
        
        if use_selenium:
            self.setup_selenium()
    
    def setup_selenium(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Selenium WebDriver initialized")
        except Exception as e:
            print(f"⚠ Selenium setup failed: {e}")
            print("Falling back to requests only")
            self.use_selenium = False
    
    def close(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
    
    def get_fund_urls_from_category(self, category_url: str) -> List[str]:
        """Extract individual fund URLs from category/AMC page"""
        fund_urls = []
        
        try:
            if self.use_selenium and self.driver:
                self.driver.get(category_url)
                time.sleep(3)  # Wait for JS to load
                
                # Find all fund links
                links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/mutual-funds/']")
                
                for link in links:
                    href = link.get_attribute('href')
                    if href and '/mutual-funds/' in href and href not in fund_urls:
                        # Exclude category/AMC pages
                        if '/category/' not in href and '/amc/' not in href:
                            fund_urls.append(href)
            else:
                # Fallback to requests
                response = requests.get(category_url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=re.compile(r'/mutual-funds/'))
                
                for link in links:
                    href = link.get('href', '')
                    if href:
                        full_url = f"https://groww.in{href}" if href.startswith('/') else href
                        if full_url not in fund_urls:
                            if '/category/' not in full_url and '/amc/' not in full_url:
                                fund_urls.append(full_url)
        
        except Exception as e:
            print(f"❌ Error extracting URLs from {category_url}: {e}")
        
        return fund_urls
    
    def scrape_fund_data(self, url: str) -> Dict:
        """
        Scrape fund data from URL
        Returns dict with all fields, using "Information not available" for missing data
        """
        fund_data = {
            "scheme_name": "Information not available",
            "expense_ratio": "Information not available",
            "lock_in": "Information not available",
            "minimum_sip": "Information not available",
            "exit_load": "Information not available",
            "riskometer": "Information not available",
            "benchmark": "Information not available",
            "nav": "Information not available",
            "fund_manager": "Information not available",
            "stamp_duty": "Information not available",
            "tax_implications": "Information not available",
            "source_url": url
        }
        
        try:
            # Try Selenium first if available
            if self.use_selenium and self.driver:
                soup = self._scrape_with_selenium(url)
            else:
                soup = self._scrape_with_requests(url)
            
            if not soup:
                return fund_data
            
            # Extract scheme name
            scheme_name = self._extract_scheme_name(soup)
            if scheme_name:
                fund_data["scheme_name"] = scheme_name
            
            # Extract all fields
            fund_data["expense_ratio"] = self._extract_expense_ratio(soup) or "Information not available"
            fund_data["lock_in"] = self._extract_lock_in(soup) or "Information not available"
            fund_data["minimum_sip"] = self._extract_minimum_sip(soup) or "Information not available"
            fund_data["exit_load"] = self._extract_exit_load(soup) or "Information not available"
            fund_data["riskometer"] = self._extract_riskometer(soup) or "Information not available"
            fund_data["benchmark"] = self._extract_benchmark(soup) or "Information not available"
            fund_data["nav"] = self._extract_nav(soup) or "Information not available"
            fund_data["fund_manager"] = self._extract_fund_manager(soup) or "Information not available"
            fund_data["stamp_duty"] = self._extract_stamp_duty(soup) or "Information not available"
            fund_data["tax_implications"] = self._extract_tax_implications(soup) or "Information not available"
            
            print(f"✅ Scraped: {fund_data['scheme_name']}")
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
        
        return fund_data
    
    def _scrape_with_selenium(self, url: str) -> Optional[BeautifulSoup]:
        """Scrape using Selenium"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for JS rendering
            
            html = self.driver.page_source
            return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            print(f"Selenium scraping failed: {e}")
            return None
    
    def _scrape_with_requests(self, url: str) -> Optional[BeautifulSoup]:
        """Scrape using requests"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Requests scraping failed: {e}")
            return None
    
    def _extract_scheme_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract scheme name"""
        # Try h1 tag - this is usually the most reliable
        h1 = soup.find('h1')
        if h1:
            name = h1.get_text(strip=True)
            # Clean up common issues
            if name.endswith('Direct Plan Growth'):
                return name
            elif 'Direct Growth' in name:
                return name
            elif len(name) > 10:  # Reasonable length
                return name
        
        # Try title tag
        title = soup.find('title')
        if title:
            text = title.get_text(strip=True)
            # Extract fund name from title (before "| Groww")
            if '|' in text:
                name = text.split('|')[0].strip()
                if len(name) > 10:
                    return name
        
        return None
    
    def _extract_expense_ratio(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract expense ratio"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'expense\s*ratio[:\s]*([\d.]+%)', re.IGNORECASE),
            re.compile(r'expense\s*ratio[:\s]*([₹\d.,]+)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_lock_in(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract lock-in period"""
        text = soup.get_text()
        
        # Check for ELSS
        if 'ELSS' in text or 'elss' in text:
            return "3 years"
        
        patterns = [
            re.compile(r'lock[- ]?in[:\s]*([\d]+\s*(?:year|month|day)s?)', re.IGNORECASE),
            re.compile(r'lock[- ]?in\s*period[:\s]*([\d]+\s*(?:year|month|day)s?)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_minimum_sip(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract minimum SIP amount"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'minimum\s*SIP[:\s]*[₹Rs\.]*\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'min\.?\s*SIP[:\s]*[₹Rs\.]*\s*([\d,]+)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                amount = match.group(1).replace(',', '')
                return f"₹{amount}"
        
        return None
    
    def _extract_exit_load(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract exit load"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'exit\s*load\s*of\s*([\d.]+%[^.]+year[^.]*?)(?:\.|$)', re.IGNORECASE),
            re.compile(r'exit\s*load[:\s]*([\d.]+%[^.]+?)(?:\.|$)', re.IGNORECASE),
            re.compile(r'([\d.]+%\s*if\s*redeemed\s*within[^.]+?)(?:\.|$)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                exit_load = match.group(1).strip()
                # Clean up extra text
                if 'Stamp duty' in exit_load:
                    exit_load = exit_load.split('Stamp duty')[0].strip()
                if exit_load.endswith('S'):
                    exit_load = exit_load[:-1].strip()
                return exit_load
        
        return None
    
    def _extract_riskometer(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract riskometer level"""
        text = soup.get_text()
        
        risk_levels = ['Very High', 'High', 'Moderately High', 'Moderate', 'Low', 'Very Low']
        
        for level in risk_levels:
            if level.lower() in text.lower():
                return level
        
        return None
    
    def _extract_benchmark(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract benchmark index"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'benchmark[:\s]*([A-Z0-9\s]+(?:Index|TRI)?)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                benchmark = match.group(1).strip()
                # Clean up
                if len(benchmark) < 50:  # Sanity check
                    return benchmark
        
        return None
    
    def _extract_nav(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract NAV"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'NAV[:\s]*[₹Rs\.]*\s*([\d,]+(?:\.\d{1,2})?)', re.IGNORECASE),
            re.compile(r'Net\s*Asset\s*Value[:\s]*[₹Rs\.]*\s*([\d,]+(?:\.\d{1,2})?)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                nav = match.group(1).strip()
                # Validate it's a reasonable NAV value
                try:
                    nav_value = float(nav.replace(',', ''))
                    if 1 < nav_value < 100000:  # Reasonable range
                        return f"₹{nav}"
                except:
                    pass
        
        return None
    
    def _extract_fund_manager(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract fund manager name"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'Fund\s*manager[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', re.IGNORECASE),
            re.compile(r'Managed\s*by[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                manager = match.group(1).strip()
                # Validate it looks like a name
                if 5 < len(manager) < 40 and manager.count(' ') >= 1:
                    return manager
        
        return None
    
    def _extract_stamp_duty(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract stamp duty"""
        text = soup.get_text()
        
        patterns = [
            re.compile(r'stamp\s*duty[:\s]*([\d.]+%\s*\(from[^)]+\))', re.IGNORECASE),
            re.compile(r'stamp\s*duty[:\s]*([\d.]+%)', re.IGNORECASE),
        ]
        
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_tax_implications(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract tax implications"""
        text = soup.get_text()
        
        # Look for tax section
        tax_pattern = re.compile(r'Tax\s*implication[s]?[:\s]*(.+?)(?:Understand|Check|Fund management|Fund size)', re.IGNORECASE | re.DOTALL)
        match = tax_pattern.search(text)
        
        if match:
            tax_text = match.group(1).strip()
            # Clean up multiple spaces and newlines
            tax_text = ' '.join(tax_text.split())
            # Limit length
            if len(tax_text) > 20:
                return tax_text[:300]
        
        return None


def main():
    """Main scraping workflow"""
    print("="*80)
    print("COMPREHENSIVE MUTUAL FUND SCRAPER")
    print("="*80)
    
    # Load URLs
    loader = URLLoader()
    urls = loader.load_urls()
    valid_urls = loader.validate_urls(urls)
    
    if not valid_urls:
        print("❌ No valid URLs found!")
        return
    
    # Initialize scraper and database
    scraper = ComprehensiveScraper(use_selenium=True)
    database = FundDatabase()
    
    try:
        # Process each URL
        for i, url in enumerate(valid_urls, 1):
            print(f"\n[{i}/{len(valid_urls)}] Processing: {url}")
            
            # Get fund URLs from category/AMC page
            fund_urls = scraper.get_fund_urls_from_category(url)
            
            if not fund_urls:
                print(f"⚠ No fund URLs found")
                continue
            
            print(f"Found {len(fund_urls)} funds")
            
            # Scrape each fund
            for j, fund_url in enumerate(fund_urls, 1):
                print(f"  [{j}/{len(fund_urls)}] Scraping: {fund_url}")
                
                fund_data = scraper.scrape_fund_data(fund_url)
                database.add_fund(fund_data)
                
                # Rate limiting
                time.sleep(2)
            
            # Save progress after each category
            database.save_database()
    
    finally:
        scraper.close()
        database.save_database()
        
        # Show statistics
        print("\n" + "="*80)
        print("SCRAPING COMPLETE")
        print("="*80)
        stats = database.get_statistics()
        print(f"Total funds: {stats['total_funds']}")
        print("\nData completeness:")
        for field, data in stats['field_completeness'].items():
            print(f"  {field}: {data['available']} ({data['percentage']:.1f}%)")


if __name__ == "__main__":
    main()
